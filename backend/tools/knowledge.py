"""
Knowledge base tools — wrap the retrieval layer for use inside the agent.
"""
from __future__ import annotations

import uuid

from backend.retrieval.context_builder import build_context
from backend.retrieval.hybrid import hybrid_search
from backend.retrieval.reranker import rerank
from backend.auth.permissions import get_permissions


async def search_knowledge(
    query: str,
    tenant_id: str,
    role: str = "employee",
    top_k: int = 5,
    **kwargs,
) -> dict:
    """
    Search the knowledge base using hybrid retrieval + reranking.
    Returns the top-K chunks formatted as context text.
    """
    from backend.database.connection import AsyncSessionLocal
    import asyncio

    perms = get_permissions(role)
    try:
        tid = uuid.UUID(tenant_id)
    except (ValueError, AttributeError):
        tid = uuid.UUID("00000000-0000-0000-0000-000000000001")

    async with AsyncSessionLocal() as session:
        candidates = await hybrid_search(
            session,
            query=query,
            tenant_id=tid,
            top_k=max(top_k * 2, 10),
            access_level=perms.max_access_level,
            departments=perms.allowed_departments,
        )

    reranked = await asyncio.to_thread(rerank, query, candidates, top_k=top_k)
    ctx = build_context(reranked)

    return {
        "query": query,
        "num_results": len(reranked),
        "context": ctx.context_text,
        "sources": [
            {
                "file_name": s.file_name,
                "department": s.department,
                "section": s.section,
                "score": round(s.score, 4),
            }
            for s in ctx.sources
        ],
    }


async def get_document(
    doc_id: str,
    tenant_id: str,
    **kwargs,
) -> dict:
    """
    Retrieve document metadata by document ID.
    """
    from backend.database.connection import AsyncSessionLocal
    from backend.database.models.documents import Document
    from sqlalchemy import select

    try:
        did = uuid.UUID(doc_id)
        tid = uuid.UUID(tenant_id)
    except (ValueError, AttributeError):
        return {"error": "Invalid doc_id or tenant_id"}

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Document).where(
                Document.id == did,
                Document.tenant_id == tid,
            )
        )
        doc = result.scalar_one_or_none()

    if doc is None:
        return {"error": f"Document {doc_id} not found"}

    return {
        "doc_id": str(doc.id),
        "file_name": doc.file_name,
        "file_type": doc.file_type,
        "department": doc.department,
        "access_level": doc.access_level,
        "version": doc.version,
        "is_latest": doc.is_latest,
        "created_at": doc.created_at.isoformat() if doc.created_at else None,
    }
