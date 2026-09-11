"""
Audit log write path.

Every significant action (login, chat, document access, approval) should
call write_audit_log() so there is an immutable record of who did what.
"""
from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.audit_logs import AuditLog


async def write_audit_log(
    session: AsyncSession,
    *,
    action: str,               # e.g. "auth.login", "chat.query", "document.access"
    resource_type: str,        # "user", "document", "conversation", "approval"
    tenant_id: uuid.UUID,
    outcome: str,              # "success" | "failure" | "denied"
    user_id: uuid.UUID | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    extra: dict | None = None,
    auto_commit: bool = False,
) -> AuditLog:
    """
    Append an audit log entry to the current session.
    Call session.commit() yourself or pass auto_commit=True.
    """
    log = AuditLog(
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        outcome=outcome,
        ip_address=ip_address,
        user_agent=user_agent,
        extra=extra or {},
        user_id=user_id,
        tenant_id=tenant_id,
    )
    session.add(log)
    if auto_commit:
        await session.commit()
        await session.refresh(log)
    return log
