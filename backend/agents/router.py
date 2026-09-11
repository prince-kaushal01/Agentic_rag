"""
Router node — decides what to do next for the current plan step.

Routing options:
  "retrieve"  — semantic/hybrid search in pgvector (knowledge base)
  "tool"      — call a registered enterprise tool (CRM, support, email)
  "answer"    — enough context gathered, generate final answer

The router uses keyword heuristics + a lightweight LLM call to classify
each plan step. LLM is only called when keywords are ambiguous.
"""
from __future__ import annotations

import os
import json
import re

from google import genai
from google.genai import types
from dotenv import load_dotenv

from backend.agents.state import AgentState

load_dotenv()

_client: genai.Client | None = None
_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# Keyword signals for fast routing (no LLM needed)
_RETRIEVE_SIGNALS = [
    "search", "find", "look up", "knowledge", "policy", "document",
    "what is", "explain", "describe", "how does", "summarize",
]
_TOOL_SIGNALS = {
    "get_customer":      ["customer", "account", "client", "acme", "corp"],
    "get_tickets":       ["ticket", "support ticket", "issue", "bug report"],
    "create_ticket":     ["create ticket", "open ticket", "file ticket", "raise ticket"],
    "draft_email":       ["draft email", "write email", "compose email", "email draft"],
    "send_email":        ["send email", "dispatch email"],
    "get_invoice":       ["invoice", "billing", "payment due", "overdue"],
}
_ANSWER_SIGNALS = [
    "draft response", "write answer", "compose reply",
    "generate answer", "final answer", "summarize findings",
]

_ROUTER_SYSTEM = """\
You are a routing agent. Given a task step description and available context,
decide what action to take next.

Reply with ONLY a JSON object:
{"action": "retrieve" | "tool" | "answer", "tool_name": "<name or null>", "reason": "<1 sentence>"}

Available tools: get_customer, get_tickets, create_ticket, draft_email, send_email, get_invoice
Use "retrieve" for knowledge base lookups.
Use "answer" only when enough context has been gathered to respond to the user.
"""


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def _keyword_route(step: str) -> tuple[str, str | None] | None:
    """Fast keyword-based routing. Returns (action, tool_name) or None."""
    step_lower = step.lower()

    # Check answer signals first
    if any(sig in step_lower for sig in _ANSWER_SIGNALS):
        return ("answer", None)

    # Check tool signals
    for tool_name, signals in _TOOL_SIGNALS.items():
        if any(sig in step_lower for sig in signals):
            return ("tool", tool_name)

    # Check retrieve signals
    if any(sig in step_lower for sig in _RETRIEVE_SIGNALS):
        return ("retrieve", None)

    return None


def router_node(state: AgentState) -> AgentState:
    """LangGraph node: decide next action for the current plan step."""
    plan = state["plan"]
    idx = state["current_step_index"]

    # If we've completed all plan steps, go to answer
    if idx >= len(plan):
        return {**state, "next_action": "answer", "tool_name": None, "tool_input": None}

    current_step = plan[idx]
    tokens = 0
    cost = 0.0

    # Try fast keyword routing first
    keyword_result = _keyword_route(current_step)

    if keyword_result:
        action, tool_name = keyword_result
        reason = f"Keyword match for '{current_step}'"
    else:
        # Fall back to LLM routing
        context_summary = (
            f"Steps completed: {len(state['steps_completed'])}\n"
            f"Sources retrieved: {len(state['retrieved_sources'])}\n"
            f"Tool results: {len(state['tool_results'])}"
        )
        prompt = (
            f"Current plan step: {current_step}\n"
            f"Context gathered so far:\n{context_summary}\n"
            f"Full user query: {state['user_query']}"
        )
        try:
            client = _get_client()
            resp = client.models.generate_content(
                model=_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=_ROUTER_SYSTEM,
                    max_output_tokens=128,
                    temperature=0.0,
                ),
            )
            raw = (resp.text or "").strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            parsed = json.loads(raw)
            action = parsed.get("action", "retrieve")
            tool_name = parsed.get("tool_name")
            reason = parsed.get("reason", "")
            tokens = resp.usage_metadata.prompt_token_count + resp.usage_metadata.candidates_token_count
            cost = round(tokens / 1_000_000 * 0.10, 6)
        except Exception:
            action, tool_name, reason = "retrieve", None, "LLM routing failed — defaulting to retrieve"

    return {
        **state,
        "next_action": action,
        "tool_name": tool_name if action == "tool" else None,
        "tool_input": {"step": current_step} if action == "tool" else None,
        "steps_used": state["steps_used"] + 1,
        "total_tokens": state["total_tokens"] + tokens,
        "total_cost_usd": state["total_cost_usd"] + cost,
        "steps_completed": [
            *state["steps_completed"],
            {
                "step_number": state["steps_used"] + 1,
                "node": "router",
                "input": current_step,
                "output": f"action={action} tool={tool_name} | {reason}",
                "tool_name": None,
                "tokens_used": tokens,
                "cost_usd": cost,
            },
        ],
    }
