"""
Planner node — decomposes the user query into an ordered list of sub-steps.

For simple single-hop questions it returns a single step.
For multi-hop tasks it returns 2-4 steps that the router will sequence through.

Examples:
  "What is the vacation policy?"
  → ["Search knowledge base for vacation policy"]

  "Draft an email to ACME Corp about their overdue invoice and create a support ticket"
  → ["Look up ACME Corp account details",
     "Check outstanding invoices for ACME Corp",
     "Draft email about overdue invoice",
     "Create support ticket for follow-up"]
"""
from __future__ import annotations

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from backend.agents.state import AgentState

load_dotenv()

_client: genai.Client | None = None
_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

_SYSTEM = """\
You are a task planning assistant for an enterprise AI agent.
Given a user query, decompose it into 1-4 concrete, ordered sub-steps the agent should execute.
Each step must be a short action phrase (≤15 words).
Return ONLY a JSON array of strings — no explanation, no markdown fences.
Example: ["Search knowledge base for refund policy", "Draft response using policy details"]
"""


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    return _client


def planner_node(state: AgentState) -> AgentState:
    """LangGraph node: generate a plan from the user query."""
    import json

    client = _get_client()
    try:
        resp = client.models.generate_content(
            model=_MODEL,
            contents=f"User query: {state['user_query']}",
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM,
                max_output_tokens=256,
                temperature=0.0,
            ),
        )
        raw = (resp.text or "").strip()
        # Strip markdown fences if model adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        plan = json.loads(raw)
        if not isinstance(plan, list) or not plan:
            raise ValueError("Empty plan")
    except Exception:
        # Fallback: single-step retrieval
        plan = [f"Search knowledge base for: {state['user_query']}"]

    tokens = 0
    cost = 0.0
    try:
        tokens = resp.usage_metadata.prompt_token_count + resp.usage_metadata.candidates_token_count
        cost = round(tokens / 1_000_000 * 0.10, 6)
    except Exception:
        pass

    return {
        **state,
        "plan": plan,
        "current_step_index": 0,
        "steps_used": state["steps_used"] + 1,
        "total_tokens": state["total_tokens"] + tokens,
        "total_cost_usd": state["total_cost_usd"] + cost,
        "steps_completed": [
            *state["steps_completed"],
            {
                "step_number": state["steps_used"] + 1,
                "node": "planner",
                "input": state["user_query"],
                "output": str(plan),
                "tool_name": None,
                "tokens_used": tokens,
                "cost_usd": cost,
            },
        ],
    }
