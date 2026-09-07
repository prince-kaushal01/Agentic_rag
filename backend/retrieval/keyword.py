"""
BM25 keyword retrieval over document chunks.

Fetches all permitted chunks from DB, builds an in-memory BM25 index,
and returns ranked results. For production scale this would use a dedicated
search engine (Elasticsearch / Typesense), but pgvector + in-process BM25
is sufficient for a corpus of ~2000 chunks.
"""
from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

from rank_bm25 import BM25Okapi
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.retrieval.semantic import RetrievedChunk, _allowed_levels


def _tokenize(text_: str) -> list[str]:
    """Simple lowercase + split on non-alphanumeric."""
    return re.findall(r"[a-z0-9]+", text_.lower())


async def keyword_search(
    session: AsyncSession,
    *,
    query: str,
    tenant_id: uuid.UUID,
    top_k: int = 6,
    access_level: str = "internal",
    departments: list[str] | None = None,
) -> list[RetrievedChunk]:
    """
    BM25 search over all permitted chunks for this tenant.
    Returns top_k results sorted by BM25 score descending.
    """
    allowed = _allowed_levels(access_level)
    dept_clause = "AND d.department = ANY(:departments)" if departments else ""

    raw_sql = text(
        f"""
        SELECT
            dc.id,
            dc.document_id,
            dc.content,
            dc.page_number,
            dc.section,
            d.file_name,
            d.department,
            d.access_level
        FROM document_chunks dc
        JOIN documents d ON d.id = dc.document_id
        WHERE
            dc.tenant_id = :tenant_id
            AND d.access_level = ANY(:allowed_levels)
            {dept_clause}
        ORDER BY dc.chunk_index
        """
    )

    params: dict = {
        "tenant_id": str(tenant_id),
        "allowed_levels": allowed,
    }
    if departments:
        params["departments"] = departments

    result = await session.execute(raw_sql, params)
    rows = result.fetchall()

    if not rows:
        return []

    # Build BM25 index
    corpus = [_tokenize(row.content) for row in rows]
    bm25 = BM25Okapi(corpus)

    query_tokens = _tokenize(query)
    scores = bm25.get_scores(query_tokens)

    # Pair (score, row) and take top_k
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]

    results = []
    for idx, score in ranked:
        if score <= 0:
            continue
        row = rows[idx]
        results.append(
            RetrievedChunk(
                chunk_id=str(row.id),
                document_id=str(row.document_id),
                content=row.content,
                score=float(score),          # raw BM25 score (not 0-1)
                page_number=row.page_number,
                section=row.section,
                department=row.department,
                access_level=row.access_level,
                file_name=row.file_name,
            )
        )

    return results
