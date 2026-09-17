"""
Task runner — creates a Task DB record, runs the LangGraph agent,
and persists the final state back to the database.

Phase 8: High-risk tool calls (risk_level >= 4) pause the agent and
create an Approval record that a manager/admin must review before the
task can resume.

Phase 9: TaskMemory snapshots agent state after each tool call so the
agent can resume after an approval decision.
"""
from __future__ import annotations

import time
import uuid
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.state import AgentState, initial_state
from backend.agents.graph import build_graph
from backend.auth.dependencies import CurrentUser
from backend.database.models.tasks import Task, TaskStatus, ToolCall
from backend.database.models.approvals import Approval, ApprovalStatus
from backend.auth.audit import write_audit_log

logger = logging.getLogger(__name__)

# Risk level at or above which we require human approval before executing
APPROVAL_RISK_THRESHOLD = 4


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

    If the agent requests a high-risk tool action (approval_required=True),
    the task is paused at TaskStatus.awaiting_approval and an Approval record
    is created for human review.  The caller receives the partially-complete
    Task so the API can return a 202-style response.
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

    # Phase 9: snapshot initial state in TaskMemory
    try:
        from backend.memory.task_memory import TaskMemory
        _task_memory_available = True
    except ImportError:
        _task_memory_available = False

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

        # 3. Build and invoke the graph
        graph = build_graph()
        final_state: AgentState = await graph.ainvoke(state)

        elapsed_ms = int((time.monotonic() - start_ms) * 1000)

        # Phase 9: save final state snapshot
        if _task_memory_available:
            try:
                await TaskMemory.save_state(str(task.id), dict(final_state))
            except Exception:
                pass  # non-critical

        # Phase 8: Check if the agent paused for approval
        if final_state.get("approval_required"):
            tool_name = final_state.get("approval_tool") or final_state.get("tool_name") or "unknown_tool"
            tool_input = final_state.get("tool_input") or {}

            # Check the tool's risk level
            try:
                from backend.tools.registry import TOOL_REGISTRY
                risk_level = TOOL_REGISTRY.get(tool_name, {}).get("risk_level", 4)
            except ImportError:
                risk_level = 4

            approval = Approval(
                task_id=task.id,
                action_type=tool_name,
                action_payload={**tool_input, "_risk_level": risk_level},
                status=ApprovalStatus.pending,
                requested_by=current_user.user_id,
                tenant_id=current_user.tenant_id,
            )
            session.add(approval)
            task.status = TaskStatus.awaiting_approval
            task.steps_completed = final_state.get("steps_completed", [])
            task.steps_used = final_state.get("steps_used", 0)
            task.total_tokens = final_state.get("total_tokens", 0)
            task.total_cost_usd = final_state.get("total_cost_usd", 0.0)
            task.latency_ms = elapsed_ms

            await write_audit_log(
                session,
                action="agent.approval_requested",
                resource_type="task",
                resource_id=str(task.id),
                tenant_id=current_user.tenant_id,
                user_id=current_user.user_id,
                outcome="pending",
                extra={"tool": tool_name, "risk_level": risk_level},
            )
            await session.commit()
            await session.refresh(task)
            return task

        # 4. Persist tool calls
        for step in final_state.get("steps_completed", []):
            if step.get("node") == "tool" and step.get("tool_name"):
                from backend.tools.registry import TOOL_REGISTRY
                rl = TOOL_REGISTRY.get(step["tool_name"], {}).get("risk_level", 1)
                tc = ToolCall(
                    tool_name=step["tool_name"],
                    input_params={"step": step.get("input")},
                    output_result={"output": step.get("output")},
                    status="success",
                    latency_ms=0,
                    risk_level=rl,
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
        logger.exception("Agent task %s failed: %s", task.id, e)

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
            "steps_used": getattr(task, "steps_used", 0),
            "cost_usd": getattr(task, "total_cost_usd", 0.0),
            "latency_ms": getattr(task, "latency_ms", 0),
        },
    )

    await session.commit()
    await session.refresh(task)
    return task
