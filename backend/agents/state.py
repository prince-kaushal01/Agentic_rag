"""
Agent state — the single object that flows through every node in the LangGraph.

TypedDict is required by LangGraph for state definitions.
All fields have defaults so the graph can be entered with just the essentials.
"""
from __future__ import annotations

import uuid
from typing import Any, Optional
from typing_extensions import TypedDict


class AgentStep(TypedDict):
    """Record of one completed step in the agent loop."""
    step_number: int
    node: str                   # "planner" | "router" | "retrieve" | "tool" | "answer"
    input: str
    output: str
    tool_name: Optional[str]
    tokens_used: int
    cost_usd: float


class SourceRef(TypedDict):
    chunk_id: str
    file_name: str
    department: Optional[str]
    section: Optional[str]
    score: float


class AgentState(TypedDict):
    # ── Identity (set at task creation, never mutated) ────────────────────────
    task_id: str
    user_id: str
    tenant_id: str
    role: str
    department: Optional[str]

    # ── Input ─────────────────────────────────────────────────────────────────
    user_query: str
    conversation_history: list[dict]   # prior messages for multi-turn context

    # ── Planning ──────────────────────────────────────────────────────────────
    plan: list[str]                    # ordered list of sub-steps to execute
    current_step_index: int

    # ── Routing decision ──────────────────────────────────────────────────────
    next_action: str                   # "retrieve" | "tool" | "answer"
    tool_name: Optional[str]           # set by router when next_action == "tool"
    tool_input: Optional[dict]

    # ── Accumulated results ───────────────────────────────────────────────────
    steps_completed: list[AgentStep]
    retrieved_sources: list[SourceRef]
    tool_results: list[dict]
    context_text: str                  # built context for LLM

    # ── Final output ──────────────────────────────────────────────────────────
    final_answer: Optional[str]
    cited_sources: list[SourceRef]

    # ── Budget & cost tracking ────────────────────────────────────────────────
    step_budget: int
    steps_used: int
    total_tokens: int
    total_cost_usd: float

    # ── Control flow ──────────────────────────────────────────────────────────
    approval_required: bool
    approval_tool: Optional[str]
    error: Optional[str]


def initial_state(
    *,
    task_id: str,
    user_id: str,
    tenant_id: str,
    role: str,
    user_query: str,
    department: str | None = None,
    conversation_history: list[dict] | None = None,
    step_budget: int = 10,
) -> AgentState:
    """Return a fully initialised AgentState ready for graph entry."""
    return AgentState(
        task_id=task_id,
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
        department=department,
        user_query=user_query,
        conversation_history=conversation_history or [],
        plan=[],
        current_step_index=0,
        next_action="retrieve",
        tool_name=None,
        tool_input=None,
        steps_completed=[],
        retrieved_sources=[],
        tool_results=[],
        context_text="",
        final_answer=None,
        cited_sources=[],
        step_budget=step_budget,
        steps_used=0,
        total_tokens=0,
        total_cost_usd=0.0,
        approval_required=False,
        approval_tool=None,
        error=None,
    )
