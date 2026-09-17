"""
Tool registry — maps tool names to handlers with risk-level enforcement,
retry logic, and timeout policy.

Risk levels:
  1 — Read       Auto-execute      search_knowledge, get_customer, get_tickets
  2 — Draft      Auto-execute      draft_email, get_document, get_customer_contract
  3 — Write      Policy-based      create_ticket
  4 — External   Approval req'd    send_email
"""
from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine

# ── Role → max allowed risk level ─────────────────────────────────────────────
_ROLE_MAX_RISK: dict[str, int] = {
    "employee":        1,
    "engineer":        2,
    "account_manager": 3,
    "manager":         3,
    "hr":              2,
    "admin":           4,
}

# ── Tool metadata ──────────────────────────────────────────────────────────────
_TOOL_META: dict[str, dict] = {
    "search_knowledge":      {"risk_level": 1, "timeout": 10},
    "get_document":          {"risk_level": 2, "timeout": 10},
    "get_customer":          {"risk_level": 1, "timeout": 8},
    "get_customer_contract": {"risk_level": 2, "timeout": 8},
    "get_tickets":           {"risk_level": 1, "timeout": 8},
    "create_ticket":         {"risk_level": 3, "timeout": 10},
    "draft_email":           {"risk_level": 2, "timeout": 15},
    "send_email":            {"risk_level": 4, "timeout": 15},
}


def _get_handler(tool_name: str) -> Callable[..., Coroutine]:
    """Lazily import tool handler to avoid circular imports."""
    if tool_name in ("search_knowledge", "get_document"):
        from backend.tools.knowledge import search_knowledge, get_document
        return {"search_knowledge": search_knowledge, "get_document": get_document}[tool_name]
    if tool_name in ("get_customer", "get_customer_contract"):
        from backend.tools.crm import get_customer, get_customer_contract
        return {"get_customer": get_customer, "get_customer_contract": get_customer_contract}[tool_name]
    if tool_name in ("get_tickets", "create_ticket"):
        from backend.tools.support import get_tickets, create_ticket
        return {"get_tickets": get_tickets, "create_ticket": create_ticket}[tool_name]
    if tool_name in ("draft_email", "send_email"):
        from backend.tools.email import draft_email, send_email
        return {"draft_email": draft_email, "send_email": send_email}[tool_name]
    raise ValueError(f"Unknown tool: {tool_name!r}")


# ── Public API ─────────────────────────────────────────────────────────────────

# Expose registry metadata for introspection
TOOL_REGISTRY = _TOOL_META


async def execute_tool(
    tool_name: str,
    params: dict,
    user_role: str,
    tenant_id: str,
) -> dict:
    """
    Dispatch a tool call with permission check, timeout, and retry.

    Returns:
        {"tool": str, "status": "success"|"error"|"permission_denied",
         "data": Any, "risk_level": int}
    """
    meta = _TOOL_META.get(tool_name)
    if meta is None:
        return {
            "tool": tool_name,
            "status": "error",
            "data": f"Tool '{tool_name}' is not registered.",
            "risk_level": 0,
        }

    risk_level: int = meta["risk_level"]
    timeout: int = meta["timeout"]
    max_role_risk = _ROLE_MAX_RISK.get(user_role, 1)

    # Permission check
    if risk_level > max_role_risk:
        return {
            "tool": tool_name,
            "status": "permission_denied",
            "data": (
                f"Role '{user_role}' cannot execute '{tool_name}' "
                f"(risk_level={risk_level}, max_allowed={max_role_risk})."
            ),
            "risk_level": risk_level,
        }

    handler = _get_handler(tool_name)

    # Retry loop (max 2 retries on transient errors)
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            result = await asyncio.wait_for(
                handler(tenant_id=tenant_id, **params),
                timeout=timeout,
            )
            return {
                "tool": tool_name,
                "status": "success",
                "data": result,
                "risk_level": risk_level,
            }
        except asyncio.TimeoutError:
            last_error = TimeoutError(f"Tool '{tool_name}' timed out after {timeout}s")
            break  # no point retrying a timeout
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                await asyncio.sleep(0.5 * (attempt + 1))

    return {
        "tool": tool_name,
        "status": "error",
        "data": str(last_error),
        "risk_level": risk_level,
    }
