"""
LangGraph agent graph.

Flow:
  planner → router → [retrieve | tool | answer]
                ↑_______________|  (loop back until budget exhausted or plan complete)

Budget guard: if steps_used >= step_budget, route to answer immediately.

Uses ainvoke so all async nodes run in the caller's event loop — no cross-loop
session issues.
"""
from __future__ import annotations

from langgraph.graph import StateGraph, END

from backend.agents.state import AgentState
from backend.agents.planner import planner_node
from backend.agents.router import router_node
from backend.agents.executor import retrieve_node, tool_node, answer_node


# ── Conditional edges ─────────────────────────────────────────────────────────

def _route_after_router(state: AgentState) -> str:
    """Edge function: map router decision to the next node name."""
    if state["steps_used"] >= state["step_budget"]:
        return "answer"
    if state.get("error"):
        return "answer"
    action = state.get("next_action", "retrieve")
    if action == "answer":
        return "answer"
    if action == "tool":
        return "tool"
    return "retrieve"


def _route_after_action(state: AgentState) -> str:
    """After retrieve/tool: go back to router for next step, or answer if done."""
    if state["steps_used"] >= state["step_budget"]:
        return "answer"
    if state.get("error"):
        return "answer"
    if state["current_step_index"] >= len(state["plan"]):
        return "answer"
    return "router"


# ── Sync wrappers for blocking planner / router nodes ─────────────────────────
# planner_node and router_node make blocking Gemini HTTP calls.
# Wrap them so they run in a thread when ainvoke drives the graph.

async def _async_planner(state: AgentState) -> AgentState:
    import asyncio
    return await asyncio.to_thread(planner_node, state)


async def _async_router(state: AgentState) -> AgentState:
    import asyncio
    return await asyncio.to_thread(router_node, state)


# ── Graph factory ─────────────────────────────────────────────────────────────

def build_graph():
    """Build and compile the agent graph. Called once per task invocation."""
    builder = StateGraph(AgentState)

    # Async nodes — run in the caller's event loop via ainvoke
    builder.add_node("planner", _async_planner)
    builder.add_node("router", _async_router)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("tool", tool_node)
    builder.add_node("answer", answer_node)

    # Entry point
    builder.set_entry_point("planner")

    # planner → router (always)
    builder.add_edge("planner", "router")

    # router → retrieve | tool | answer (conditional)
    builder.add_conditional_edges(
        "router",
        _route_after_router,
        {"retrieve": "retrieve", "tool": "tool", "answer": "answer"},
    )

    # retrieve → router | answer (conditional)
    builder.add_conditional_edges(
        "retrieve",
        _route_after_action,
        {"router": "router", "answer": "answer"},
    )

    # tool → router | answer (conditional)
    builder.add_conditional_edges(
        "tool",
        _route_after_action,
        {"router": "router", "answer": "answer"},
    )

    # answer → END
    builder.add_edge("answer", END)

    return builder.compile()
