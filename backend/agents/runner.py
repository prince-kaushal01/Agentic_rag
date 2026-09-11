"""
Task runner — creates a Task DB record, runs the LangGraph agent,
and persists the final state back to the database.
"""
from __future__ import annotations

import time
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.state import AgentState, initial_state
from backend.agents.graph import build_graph
from backend.auth.dependencies import CurrentUser
from backend.database.models.tasks import Task, TaskStatus, ToolCall
from backend.auth.audit import write_audit_log


async def run_agent_task(
    session: AsyncSession,
    *,
    user_query: str,
    current_user: CurrentUser,
    conversation_id: uuid.UUID | None = None,
    step_budget: int = 10,
    conversation_history: list[dict] | None = None,
) -> Task:
    """
    Create a Task, run the agent graph, persist results, return the Task.
    """
    # 1. Create Task record
    task = Task(
        description=user_query[:500],
        status=TaskStatus.running,
        step_budget=step_budget,
        steps_used=0,
        user_id=current_user.user_id,
        tenant_id=current_user.tenant_id,
        conversation_id=conversation_id,
    )
    session.add(task)
    await session.flush()   # get task.id

    start_ms = time.monotonic()

    try:
        # 2. Build initial state
        state = initial_state(
            task_id=str(task.id),
            user_id=str(current_user.user_id),
            tenant_id=str(current_user.tenant_id),
            role=current_user.role,
            department=current_user.department,
            user_query=user_query,
            conversation_history=conversation_history or [],
            step_budget=step_budget,
        )

        # 3. Build and invoke the graph (async — runs in FastAPI's event loop)
        graph = build_graph()
        final_state: AgentState = await graph.ainvoke(state)

        elapsed_ms = int((time.monotonic() - start_ms) * 1000)

        # 4. Persist tool calls
        for step in final_state.get("steps_completed", []):
            if step.get("node") == "tool" and step.get("tool_name"):
                tc = ToolCall(
                    tool_name=step["tool_name"],
                    input_params={"step": step.get("input")},
                    output_result={"output": step.get("output")},
                    status="success",
                    latency_ms=0,
                    risk_level=1,
                    task_id=task.id,
                    tenant_id=current_user.tenant_id,
                )
                session.add(tc)

        # 5. Update task record
        task.status = TaskStatus.completed
        task.final_answer = final_state.get("final_answer")
        task.steps_completed = final_state.get("steps_completed", [])
        task.retrieved_sources = final_state.get("retrieved_sources", [])
        task.tool_results = final_state.get("tool_results", [])
        task.steps_used = final_state.get("steps_used", 0)
        task.total_tokens = final_state.get("total_tokens", 0)
        task.total_cost_usd = final_state.get("total_cost_usd", 0.0)
        task.latency_ms = elapsed_ms

    except Exception as e:
        elapsed_ms = int((time.monotonic() - start_ms) * 1000)
        task.status = TaskStatus.failed
        task.error_message = str(e)
        task.latency_ms = elapsed_ms

    # 6. Audit log
    await write_audit_log(
        session,
        action="agent.task",
        resource_type="task",
        resource_id=str(task.id),
        tenant_id=current_user.tenant_id,
        user_id=current_user.user_id,
        outcome="success" if task.status == TaskStatus.completed else "failure",
        extra={
            "steps_used": task.steps_used,
            "cost_usd": task.total_cost_usd,
            "latency_ms": task.latency_ms,
        },
    )

    await session.commit()
    await session.refresh(task)
    return task
