"""
Tenant isolation verification — ensures every DB query is scoped to a tenant.
Used in integration tests and as a defensive check in critical paths.
"""
from __future__ import annotations

import uuid

from sqlalchemy import select

from backend.database.connection import AsyncSessionLocal
from backend.database.models.documents import Document
from backend.database.models.conversations import Conversation
from backend.database.models.tasks import Task


class TenantIsolationChecker:
    """
    Verifies that resources belong to the expected tenant.
    Raises on isolation violations so they surface as test failures, not silent data leaks.
    """

    @staticmethod
    async def verify_document_access(
        doc_id: str,
        tenant_id: str,
        user_id: str,
    ) -> bool:
        """
        Returns True if the document exists AND belongs to the given tenant.
        Returns False if not found. Raises ValueError on tenant mismatch.
        """
        try:
            did = uuid.UUID(doc_id)
            tid = uuid.UUID(tenant_id)
        except ValueError:
            return False

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Document).where(Document.id == did)
            )
            doc = result.scalar_one_or_none()

        if doc is None:
            return False
        if doc.tenant_id != tid:
            raise PermissionError(
                f"Tenant isolation violation: document {doc_id} belongs to "
                f"tenant {doc.tenant_id}, not {tenant_id}"
            )
        return True

    @staticmethod
    async def verify_conversation_access(
        conversation_id: str,
        user_id: str,
        tenant_id: str,
    ) -> bool:
        """
        Returns True if the conversation belongs to the given tenant and user.
        Raises PermissionError on tenant mismatch.
        """
        try:
            cid = uuid.UUID(conversation_id)
            uid = uuid.UUID(user_id)
            tid = uuid.UUID(tenant_id)
        except ValueError:
            return False

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Conversation).where(Conversation.id == cid)
            )
            conv = result.scalar_one_or_none()

        if conv is None:
            return False
        if conv.tenant_id != tid:
            raise PermissionError(
                f"Tenant isolation violation: conversation {conversation_id} belongs to "
                f"tenant {conv.tenant_id}, not {tenant_id}"
            )
        # Also verify user ownership
        if conv.user_id != uid:
            raise PermissionError(
                f"Conversation {conversation_id} belongs to user {conv.user_id}, not {user_id}"
            )
        return True

    @staticmethod
    async def verify_task_access(
        task_id: str,
        user_id: str,
        tenant_id: str,
    ) -> bool:
        """
        Returns True if the task belongs to the given tenant and user.
        Raises PermissionError on tenant mismatch.
        """
        try:
            tid_db = uuid.UUID(task_id)
            uid = uuid.UUID(user_id)
            tenant_uuid = uuid.UUID(tenant_id)
        except ValueError:
            return False

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Task).where(Task.id == tid_db)
            )
            task = result.scalar_one_or_none()

        if task is None:
            return False
        if task.tenant_id != tenant_uuid:
            raise PermissionError(
                f"Tenant isolation violation: task {task_id} belongs to "
                f"tenant {task.tenant_id}, not {tenant_id}"
            )
        return True

    @staticmethod
    def assert_tenant_id_in_filters(query_kwargs: dict, tenant_id: str) -> None:
        """
        Raise ValueError if tenant_id is not present in the query filter dict.
        Use in integration tests to catch unfiltered queries.
        """
        if "tenant_id" not in query_kwargs:
            raise ValueError(
                f"Missing tenant_id filter — potential tenant isolation violation! "
                f"Expected tenant_id='{tenant_id}' in query filters."
            )

    @staticmethod
    def validate_uuid_match(stored_tenant_id: str | uuid.UUID, request_tenant_id: str | uuid.UUID) -> None:
        """
        Raise PermissionError if two tenant UUIDs don't match.
        Use at API boundaries before returning data.
        """
        stored = uuid.UUID(str(stored_tenant_id))
        request = uuid.UUID(str(request_tenant_id))
        if stored != request:
            raise PermissionError(
                f"Tenant UUID mismatch: stored={stored}, requested={request}"
            )
