"""
Executor nodes — one per action type:

  retrieve_node  — run hybrid search + rerank, append to context
  tool_node      — dispatch to the tool registry (Phase 7), stubs for now
  answer_node    — call LLM with all accumulated context, produce final answer

Each node creates its own DB session so it is safe to call from any event loop.
"""
from __future__ import annotations

import asyncio
import uuid

from backend.agents.state import AgentState, SourceRef
from backend.retrieval.hybrid import hybrid_search
from backend.retrieval.reranker import rerank
from backend.retrieval.context_builder import build_context
from backend.retrieval.llm import answer_with_context
from backend.auth.permissions import get_permissions


# ── Retrieve node ─────────────────────────────────────────────────────────────

async def retrieve_node(state: AgentState) -> AgentState:
    """Run hybrid search for the current plan step and accumulate context."""
    from backend.database.connection import AsyncSessionLocal

    plan = state["plan"]
    idx = state["current_step_index"]
    step_query = plan[idx] if idx < len(plan) else state["user_query"]

    perms = get_permissions(state["role"])

    async with AsyncSessionLocal() as session:
        candidates = await hybrid_search(
            session,
            query=step_query,
            tenant_id=uuid.UUID(state["tenant_id"]),
            top_k=12,
            access_level=perms.max_access_level,
            departments=perms.allowed_departments,
            semantic_k=12,
            keyword_k=12,
        )

    # Rerank in a thread (CPU-bound)
    reranked = await asyncio.to_thread(rerank, step_query, candidates, top_k=5)

    # Build context from this retrieval step
    ctx = build_context(reranked)

    # Accumulate sources (deduplicate by chunk_id)
    existing_ids = {s["chunk_id"] for s in state["retrieved_sources"]}
    new_sources: list[SourceRef] = [
        SourceRef(
            chunk_id=src.chunk_id,
            file_name=src.file_name,
            department=src.department,
            section=src.section,
            score=src.score,
        )
        for src in ctx.sources
        if src.chunk_id not in existing_ids
    ]

    # Append to accumulated context (separated by step label)
    step_label = f"\n\n### Step {idx + 1}: {step_query}\n\n"
    updated_context = state["context_text"] + step_label + ctx.context_text

    return {
        **state,
        "retrieved_sources": [*state["retrieved_sources"], *new_sources],
        "context_text": updated_context,
        "current_step_index": idx + 1,
        "steps_used": state["steps_used"] + 1,
        "steps_completed": [
            *state["steps_completed"],
            {
                "step_number": state["steps_used"] + 1,
                "node": "retrieve",
                "input": step_query,
                "output": f"{len(reranked)} chunks retrieved, {ctx.total_chars} chars",
                "tool_name": None,
                "tokens_used": 0,
                "cost_usd": 0.0,
            },
        ],
    }


# ── Tool node ─────────────────────────────────────────────────────────────────

async def tool_node(state: AgentState) -> AgentState:
    """
    Dispatch to tool registry.
    Phase 7 will wire in real tools — this node provides the interface contract.
    Stubs return realistic fake data so the agent can still produce answers.
    """
    tool_name = state.get("tool_name") or "unknown"
    tool_input = state.get("tool_input") or {}
    plan = state["plan"]
    idx = state["current_step_index"]

    # Phase 7 tool registry hook — import lazily so it's optional
    result: dict
    try:
        from backend.tools.registry import execute_tool
        result = await execute_tool(
            tool_name=tool_name,
            params=tool_input,
            user_role=state["role"],
            tenant_id=state["tenant_id"],
        )
    except ImportError:
        # Tool registry not yet built — return a stub
        result = {
            "tool": tool_name,
            "status": "stub",
            "data": f"[Tool '{tool_name}' called with {tool_input}. Phase 7 will wire real results.]",
        }
    except Exception as e:
        result = {"tool": tool_name, "status": "error", "error": str(e)}

    # Append result to context so the answer node can use it
    tool_block = (
        f"\n\n### Tool Result: {tool_name}\n"
        f"{result.get('data', str(result))}\n"
    )

    return {
        **state,
        "tool_results": [*state["tool_results"], {"tool": tool_name, "result": result}],
        "context_text": state["context_text"] + tool_block,
        "current_step_index": idx + 1,
        "steps_used": state["steps_used"] + 1,
        "steps_completed": [
            *state["steps_completed"],
            {
                "step_number": state["steps_used"] + 1,
                "node": "tool",
                "input": str(tool_input),
                "output": str(result),
                "tool_name": tool_name,
                "tokens_used": 0,
                "cost_usd": 0.0,
            },
        ],
    }


# ── Answer node ───────────────────────────────────────────────────────────────

async def answer_node(state: AgentState) -> AgentState:
    """Generate the final answer using all accumulated context."""
    from backend.retrieval.context_builder import BuiltContext, SourceCitation

    # Rebuild a BuiltContext from accumulated state
    sources = [
        SourceCitation(
            chunk_id=s["chunk_id"],
            document_id=s["chunk_id"],   # chunk_id used as proxy
            file_name=s["file_name"],
            department=s.get("department"),
            section=s.get("section"),
            page_number=None,
            score=s["score"],
        )
        for s in state["retrieved_sources"]
    ]

    ctx = BuiltContext(
        context_text=state["context_text"],
        sources=sources,
        total_chars=len(state["context_text"]),
    )

    llm_resp = await asyncio.to_thread(
        answer_with_context,
        state["user_query"],
        ctx,
        state["conversation_history"],
    )

    # Map citation indices to sources
    cited: list[SourceRef] = []
    for idx in llm_resp.cited_indices:
        if 1 <= idx <= len(sources):
            src = sources[idx - 1]
            cited.append(SourceRef(
                chunk_id=src.chunk_id,
                file_name=src.file_name,
                department=src.department,
                section=src.section,
                score=src.score,
            ))
    if not cited:
        cited = list(state["retrieved_sources"][:3])

    return {
        **state,
        "final_answer": llm_resp.answer,
        "cited_sources": cited,
        "steps_used": state["steps_used"] + 1,
        "total_tokens": state["total_tokens"] + llm_resp.input_tokens + llm_resp.output_tokens,
        "total_cost_usd": state["total_cost_usd"] + llm_resp.cost_usd,
        "steps_completed": [
            *state["steps_completed"],
            {
                "step_number": state["steps_used"] + 1,
                "node": "answer",
                "input": state["user_query"],
                "output": llm_resp.answer[:200],
                "tool_name": None,
                "tokens_used": llm_resp.input_tokens + llm_resp.output_tokens,
                "cost_usd": llm_resp.cost_usd,
            },
        ],
    }
