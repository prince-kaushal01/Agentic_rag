"""
Semantic retrieval using pgvector cosine similarity.

Filters applied at the DB level:
  - tenant_id   — hard multi-tenant isolation
  - access_level — public < internal < confidential < restricted
  - department  — optional whitelist
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.documents import DocumentChunk, AccessLevel
from ingestion.embeddings.embedder import embed_query


# Access level hierarchy — a user at level N can see levels 0..N
_LEVEL_ORDER = [
    AccessLevel.public,
    AccessLevel.internal,
    AccessLevel.confidential,
    AccessLevel.restricted,
]


def _allowed_levels(max_level: str) -> list[str]:
    """Return all AccessLevel values the user is permitted to see."""
    try:
        idx = _LEVEL_ORDER.index(AccessLevel(max_level))
    except ValueError:
        idx = 1  # default to internal
    return [lvl.value for lvl in _LEVEL_ORDER[: idx + 1]]


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    content: str
    score: float          # cosine similarity 0-1
    page_number: int | None
    section: str | None
    department: str | None
    access_level: str
    file_name: str        # populated via join


async def semantic_search(
    session: AsyncSession,
    *,
    query: str,
    tenant_id: uuid.UUID,
    top_k: int = 6,
    access_level: str = "internal",          # max level the caller may see
    departments: list[str] | None = None,    # None = all permitted departments
) -> list[RetrievedChunk]:
    """
    Embed the query and return the top-K most similar chunks
    that pass the tenant + ACL filters.
    """
    query_vec = embed_query(query)
    allowed = _allowed_levels(access_level)

    # Build the pgvector cosine similarity query
    # 1 - (embedding <=> :vec) gives similarity in [0, 1]
    stmt = (
        select(
            DocumentChunk,
            text("1 - (dc.embedding <=> CAST(:vec AS vector)) AS score"),
        )
        .select_from(text("document_chunks dc"))
        .join(
            DocumentChunk,
            text("dc.id = document_chunks.id"),
            isouter=False,
        )
    )

    # Simpler approach using ORM directly with cast
    vec_literal = f"[{','.join(str(v) for v in query_vec)}]"

    # Build department filter conditionally — asyncpg can't infer type of NULL in ANY()
    dept_clause = "AND d.department = ANY(:departments)" if departments else ""

    raw_sql = text(
        f"""
        SELECT
            dc.id,
            dc.document_id,
            dc.content,
            dc.page_number,
            dc.section,
            dc.token_count,
            dc.chunk_metadata,
            dc.tenant_id,
            d.file_name,
            d.department,
            d.access_level,
            1 - (dc.embedding <=> CAST(:vec AS vector)) AS score
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        WHERE
            dc.tenant_id = :tenant_id
            AND d.access_level = ANY(:allowed_levels)
            {dept_clause}
        ORDER BY dc.embedding <=> CAST(:vec AS vector)
        LIMIT :top_k
        """
    )

    params: dict = {
        "vec": vec_literal,
        "tenant_id": str(tenant_id),
        "allowed_levels": allowed,
        "top_k": top_k,
    }
    if departments:
        params["departments"] = departments

    result = await session.execute(raw_sql, params)
    rows = result.fetchall()

    return [
        RetrievedChunk(
            chunk_id=str(row.id),
            document_id=str(row.document_id),
            content=row.content,
            score=float(row.score),
            page_number=row.page_number,
            section=row.section,
            department=row.department,
            access_level=row.access_level,
            file_name=row.file_name,
        )
        for row in rows
    ]
