"""
Simulated support ticket tools — synthetic NovaTech support data.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

# ── Synthetic ticket data ──────────────────────────────────────────────────────

_TICKETS: dict[str, list[dict]] = {
    "CUST-001": [
        {
            "id": "TKT-10042",
            "customer_id": "CUST-001",
            "subject": "API rate limiting causing pipeline failures",
            "description": "Our nightly ETL jobs are being throttled at peak hours, causing data sync to fail.",
            "priority": "high",
            "status": "open",
            "category": "technical",
            "assignee": "Alex Kim",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat(),
        },
        {
            "id": "TKT-10038",
            "customer_id": "CUST-001",
            "subject": "SSO integration setup assistance",
            "description": "Need help configuring SAML 2.0 with Okta for 500 users.",
            "priority": "medium",
            "status": "in_progress",
            "category": "onboarding",
            "assignee": "Morgan Lee",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        },
    ],
    "CUST-002": [
        {
            "id": "TKT-10055",
            "customer_id": "CUST-002",
            "subject": "Vector search returning stale results",
            "description": "Recently ingested documents not appearing in search for ~15 minutes.",
            "priority": "medium",
            "status": "open",
            "category": "technical",
            "assignee": "Alex Kim",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) + timedelta(hours=12)).isoformat(),
        },
    ],
    "CUST-003": [
        {
            "id": "TKT-10011",
            "customer_id": "CUST-003",
            "subject": "Data residency compliance — EU data must stay in EU",
            "description": "Audit team requires confirmation that all customer data is stored in EU region only.",
            "priority": "critical",
            "status": "escalated",
            "category": "compliance",
            "assignee": "Jamie Walsh",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=14)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "sla_breached": True,
        },
        {
            "id": "TKT-10029",
            "customer_id": "CUST-003",
            "subject": "Billing discrepancy on November invoice",
            "description": "Invoice shows 1,200 seats billed but contract specifies 1,000.",
            "priority": "high",
            "status": "open",
            "category": "billing",
            "assignee": "Casey Brooks",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) + timedelta(hours=18)).isoformat(),
        },
    ],
    "CUST-005": [
        {
            "id": "TKT-10061",
            "customer_id": "CUST-005",
            "subject": "BAA addendum review — legal sign-off needed",
            "description": "HIPAA Business Associate Agreement addendum awaiting NovaTech legal review.",
            "priority": "high",
            "status": "open",
            "category": "legal",
            "assignee": "Jamie Walsh",
            "created_at": (datetime.now(timezone.utc) - timedelta(days=4)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "sla_breach_at": (datetime.now(timezone.utc) + timedelta(days=3)).isoformat(),
        },
    ],
}

# In-memory store for newly created tickets (resets on restart — simulated)
_CREATED_TICKETS: list[dict] = []


async def get_tickets(
    customer_id: str | None = None,
    status: str = "all",
    priority: str | None = None,
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """
    Retrieve support tickets. Filter by customer, status, or priority.
    If no customer_id, returns all tickets across customers.
    """
    all_tickets: list[dict] = []

    if customer_id:
        cid = customer_id.upper()
        # Try direct lookup, then fuzzy search across IDs
        found_tickets = _TICKETS.get(cid, [])
        if not found_tickets:
            # Try matching by partial ID or customer name lookup
            for k, v in _TICKETS.items():
                if customer_id.lower() in k.lower():
                    found_tickets.extend(v)
        all_tickets = found_tickets
    else:
        for tickets in _TICKETS.values():
            all_tickets.extend(tickets)

    # Include newly created tickets
    all_tickets = all_tickets + [
        t for t in _CREATED_TICKETS
        if not customer_id or t.get("customer_id", "").upper() == customer_id.upper()
    ]

    # Apply filters
    if status and status != "all":
        all_tickets = [t for t in all_tickets if t["status"] == status]
    if priority:
        all_tickets = [t for t in all_tickets if t["priority"] == priority]

    return {
        "total": len(all_tickets),
        "customer_id": customer_id or "all",
        "status_filter": status,
        "tickets": all_tickets,
    }


async def create_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "medium",
    category: str = "general",
    tenant_id: str = "",
    **kwargs,
) -> dict:
    """
    Create a new support ticket (simulated — stored in-memory).
    Returns ticket ID and confirmation details.
    """
    valid_priorities = {"low", "medium", "high", "critical"}
    if priority not in valid_priorities:
        priority = "medium"

    ticket_num = 10100 + len(_CREATED_TICKETS)
    ticket = {
        "id": f"TKT-{ticket_num}",
        "customer_id": customer_id.upper(),
        "subject": subject,
        "description": description,
        "priority": priority,
        "status": "open",
        "category": category,
        "assignee": "Auto-assigned (pending)",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "sla_breach_at": (
            datetime.now(timezone.utc) + timedelta(
                hours={"critical": 4, "high": 8, "medium": 24, "low": 72}.get(priority, 24)
            )
        ).isoformat(),
        "source": "agent_created",
    }
    _CREATED_TICKETS.append(ticket)

    return {
        "created": True,
        "ticket_id": ticket["id"],
        "customer_id": customer_id,
        "subject": subject,
        "priority": priority,
        "status": "open",
        "message": (
            f"Ticket {ticket['id']} created successfully for {customer_id}. "
            f"SLA response due within "
            f"{'4 hours' if priority == 'critical' else '8 hours' if priority == 'high' else '24 hours'}."
        ),
        "ticket": ticket,
    }
