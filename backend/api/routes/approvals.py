"""
Approval endpoints — human-in-the-loop review for Level 3/4 tool actions.

Flow:
  1. Agent encounters a high-risk tool → sets approval_required=True in state
  2. Runner creates an Approval record → task status = awaiting_approval
  3. User calls GET /approvals or GET /approvals/{id} to review
  4. User calls POST /approvals/{id}/approve or /reject
  5. Task status flips back to "running" so the agent can resume
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.dependencies import get_current_user, CurrentUser
from backend.auth.audit import write_audit_log
from backend.database.connection import AsyncSessionLocal
from backend.database.models.approvals import Approval, ApprovalStatus
from backend.database.models.tasks import Task, TaskStatus

router = APIRouter(prefix="/approvals", tags=["approvals"])


# ── Pydantic schemas ───────────────────────────────────────────────────────────

class ApproveRequest(BaseModel):
    edited_payload: dict | None = None
    review_note: str = ""


class RejectRequest(BaseModel):
    review_note: str = ""


class ApprovalOut(BaseModel):
    id: str
    task_id: str
    action_type: str
    action_payload: dict | None
    edited_payload: dict | None
    status: str
    review_note: str | None
    reviewed_at: str | None
    requested_by: str
    reviewed_by: str | None
    created_at: str | None


def _approval_out(a: Approval) -> ApprovalOut:
    return ApprovalOut(
        id=str(a.id),
        task_id=str(a.task_id),
        action_type=a.action_type,
        action_payload=a.action_payload,
        edited_payload=a.edited_payload,
        status=a.status.value,
        review_note=a.review_note,
        reviewed_at=a.reviewed_at.isoformat() if a.reviewed_at else None,
        requested_by=str(a.requested_by),
        reviewed_by=str(a.reviewed_by) if a.reviewed_by else None,
        created_at=a.created_at.isoformat() if hasattr(a, "created_at") and a.created_at else None,
    )


# ── Helper: get DB session ─────────────────────────────────────────────────────

async def _get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ── Routes ─────────────────────────────────────────────────────────────────────

@router.get("", response_model=list[ApprovalOut])
async def list_approvals(
    status_filter: str = "pending",
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(_get_session),
):
    """
    List approvals for the current tenant.
    Managers/admins see all; others see only their own.
    """
    q = select(Approval).where(Approval.tenant_id == current_user.tenant_id)

    if current_user.role not in ("admin", "manager"):
        q = q.where(Approval.requested_by == current_user.user_id)

    if status_filter != "all":
        try:
            q = q.where(Approval.status == ApprovalStatus(status_filter))
        except ValueError:
            pass  # ignore invalid filter

    q = q.order_by(Approval.created_at.desc()).limit(50)
    result = await session.execute(q)
    approvals = result.scalars().all()
    return [_approval_out(a) for a in approvals]


@router.get("/{approval_id}", response_model=ApprovalOut)
async def get_approval(
    approval_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(_get_session),
):
    """Get a single approval by ID."""
    try:
        aid = uuid.UUID(approval_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid approval ID")

    result = await session.execute(
        select(Approval).where(
            Approval.id == aid,
            Approval.tenant_id == current_user.tenant_id,
        )
    )
    approval = result.scalar_one_or_none()
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")

    # Non-managers can only see their own
    if current_user.role not in ("admin", "manager") and approval.requested_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return _approval_out(approval)


@router.post("/{approval_id}/approve", response_model=ApprovalOut)
async def approve_action(
    approval_id: str,
    body: ApproveRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(_get_session),
):
    """
    Approve a pending action. Optionally supply an edited payload.
    Resumes the parent task.
    """
    if current_user.role not in ("admin", "manager", "hr", "account_manager"):
        raise HTTPException(status_code=403, detail="Insufficient role to approve actions")

    try:
        aid = uuid.UUID(approval_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid approval ID")

    result = await session.execute(
        select(Approval).where(
            Approval.id == aid,
            Approval.tenant_id == current_user.tenant_id,
        )
    )
    approval = result.scalar_one_or_none()
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")

    if approval.status != ApprovalStatus.pending:
        raise HTTPException(
            status_code=409,
            detail=f"Approval is already '{approval.status.value}', cannot approve again",
        )

    # Update approval
    if body.edited_payload:
        approval.status = ApprovalStatus.edited_and_approved
        approval.edited_payload = body.edited_payload
    else:
        approval.status = ApprovalStatus.approved

    approval.reviewed_by = current_user.user_id
    approval.reviewed_at = datetime.now(timezone.utc)
    approval.review_note = body.review_note or None

    # Resume parent task
    task_result = await session.execute(
        select(Task).where(Task.id == approval.task_id)
    )
    task = task_result.scalar_one_or_none()
    if task and task.status == TaskStatus.awaiting_approval:
        task.status = TaskStatus.running

    await write_audit_log(
        session,
        action="approval.approved",
        resource_type="approval",
        resource_id=str(aid),
        tenant_id=current_user.tenant_id,
        user_id=current_user.user_id,
        outcome="success",
        extra={"action_type": approval.action_type, "edited": bool(body.edited_payload)},
    )

    await session.commit()
    await session.refresh(approval)
    return _approval_out(approval)


@router.post("/{approval_id}/reject", response_model=ApprovalOut)
async def reject_action(
    approval_id: str,
    body: RejectRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(_get_session),
):
    """
    Reject a pending action. The parent task is marked as cancelled.
    """
    if current_user.role not in ("admin", "manager", "hr", "account_manager"):
        raise HTTPException(status_code=403, detail="Insufficient role to reject actions")

    try:
        aid = uuid.UUID(approval_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid approval ID")

    result = await session.execute(
        select(Approval).where(
            Approval.id == aid,
            Approval.tenant_id == current_user.tenant_id,
        )
    )
    approval = result.scalar_one_or_none()
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")

    if approval.status != ApprovalStatus.pending:
        raise HTTPException(
            status_code=409,
            detail=f"Approval is already '{approval.status.value}', cannot reject",
        )

    approval.status = ApprovalStatus.rejected
    approval.reviewed_by = current_user.user_id
    approval.reviewed_at = datetime.now(timezone.utc)
    approval.review_note = body.review_note or "Rejected without comment"

    # Mark parent task as cancelled
    task_result = await session.execute(
        select(Task).where(Task.id == approval.task_id)
    )
    task = task_result.scalar_one_or_none()
    if task and task.status == TaskStatus.awaiting_approval:
        task.status = TaskStatus.cancelled

    await write_audit_log(
        session,
        action="approval.rejected",
        resource_type="approval",
        resource_id=str(aid),
        tenant_id=current_user.tenant_id,
        user_id=current_user.user_id,
        outcome="success",
        extra={"action_type": approval.action_type, "note": body.review_note},
    )

    await session.commit()
    await session.refresh(approval)
    return _approval_out(approval)
