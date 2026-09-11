"""
Task API routes.

POST /tasks          — Create and run an agentic task
GET  /tasks/{id}     — Get task status + result
GET  /tasks          — List tasks for the current user
GET  /tasks/{id}/trace  — Get full step-by-step trace
"""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.connection import AsyncSessionLocal
from backend.database.models.tasks import Task, TaskStatus
from backend.auth.dependencies import get_current_user, CurrentUser
from backend.agents.runner import run_agent_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


# ── DB session ────────────────────────────────────────────────────────────────

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ── Schemas ───────────────────────────────────────────────────────────────────

class TaskCreateRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    step_budget: int = Field(default=8, ge=1, le=15)


class TaskStepOut(BaseModel):
    step_number: int
    node: str
    input: str
    output: str
    tool_name: Optional[str]
    tokens_used: int
    cost_usd: float


class TaskOut(BaseModel):
    task_id: str
    status: str
    description: str
    final_answer: Optional[str]
    steps_used: int
    step_budget: int
    total_tokens: Optional[int]
    total_cost_usd: Optional[float]
    latency_ms: Optional[int]
    sources: list[dict]
    tool_results: list[dict]
    error_message: Optional[str]


class TaskTraceOut(BaseModel):
    task_id: str
    status: str
    steps: list[TaskStepOut]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=TaskOut, status_code=201)
async def create_task(
    req: TaskCreateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    """Run an agentic task and return the result when complete."""
    conv_id = uuid.UUID(req.conversation_id) if req.conversation_id else None

    task = await run_agent_task(
        session,
        user_query=req.query,
        current_user=current_user,
        conversation_id=conv_id,
        step_budget=req.step_budget,
    )

    return _task_to_out(task)


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
    limit: int = 20,
):
    result = await session.execute(
        select(Task)
        .where(Task.user_id == current_user.user_id)
        .where(Task.tenant_id == current_user.tenant_id)
        .order_by(Task.created_at.desc())
        .limit(limit)
    )
    tasks = result.scalars().all()
    return [_task_to_out(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    task = await _load_task(session, task_id, current_user)
    return _task_to_out(task)


@router.get("/{task_id}/trace", response_model=TaskTraceOut)
async def get_task_trace(
    task_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
):
    task = await _load_task(session, task_id, current_user)
    steps = [
        TaskStepOut(
            step_number=s.get("step_number", 0),
            node=s.get("node", ""),
            input=s.get("input", ""),
            output=s.get("output", ""),
            tool_name=s.get("tool_name"),
            tokens_used=s.get("tokens_used", 0),
            cost_usd=s.get("cost_usd", 0.0),
        )
        for s in (task.steps_completed or [])
    ]
    return TaskTraceOut(task_id=str(task.id), status=task.status.value, steps=steps)


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _load_task(session: AsyncSession, task_id: str, user: CurrentUser) -> Task:
    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = await session.execute(
        select(Task)
        .where(Task.id == tid)
        .where(Task.tenant_id == user.tenant_id)
    )
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def _task_to_out(task: Task) -> TaskOut:
    return TaskOut(
        task_id=str(task.id),
        status=task.status.value,
        description=task.description,
        final_answer=task.final_answer,
        steps_used=task.steps_used or 0,
        step_budget=task.step_budget,
        total_tokens=task.total_tokens,
        total_cost_usd=task.total_cost_usd,
        latency_ms=task.latency_ms,
        sources=task.retrieved_sources or [],
        tool_results=task.tool_results or [],
        error_message=task.error_message,
    )
