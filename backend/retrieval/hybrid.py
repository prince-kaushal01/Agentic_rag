"""
Hybrid retrieval: semantic + BM25 fused via Reciprocal Rank Fusion (RRF).

RRF formula:  score(d) = Σ  1 / (k + rank_i(d))
              where k=60 is a smoothing constant.

The fused list is then optionally reranked by a cross-encoder.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.retrieval.semantic import RetrievedChunk, semantic_search
from backend.retrieval.keyword import keyword_search

# RRF smoothing constant — standard value from the original paper
_RRF_K = 60


def reciprocal_rank_fusion(
    *ranked_lists: list[RetrievedChunk],
    top_k: int = 10,
) -> list[RetrievedChunk]:
    """
    Merge multiple ranked lists using RRF.
    Returns a new list of RetrievedChunk with score = RRF score.
    Deduplication by chunk_id — keeps the first occurrence's metadata.
    """
    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, RetrievedChunk] = {}

    for ranked in ranked_lists:
        for rank, chunk in enumerate(ranked, start=1):
            cid = chunk.chunk_id
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (_RRF_K + rank)
            if cid not in chunk_map:
                chunk_map[cid] = chunk

    # Sort by RRF score descending
    sorted_ids = sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)

    results = []
    for cid in sorted_ids[:top_k]:
        chunk = chunk_map[cid]
        # Replace score field with the RRF score for downstream display
        results.append(
            RetrievedChunk(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=chunk.content,
                score=round(rrf_scores[cid], 6),
                page_number=chunk.page_number,
                section=chunk.section,
                department=chunk.department,
                access_level=chunk.access_level,
                file_name=chunk.file_name,
            )
        )

    return results


async def hybrid_search(
    session: AsyncSession,
    *,
    query: str,
    tenant_id: uuid.UUID,
    top_k: int = 8,
    access_level: str = "internal",
    departments: list[str] | None = None,
    semantic_k: int = 20,   # wider net before fusion
    keyword_k: int = 20,
) -> list[RetrievedChunk]:
    """
    Run semantic + BM25 in parallel, fuse with RRF, return top_k.
    """
    # Run sequentially — SQLAlchemy async sessions don't allow concurrent queries
    semantic_results = await semantic_search(
        session,
        query=query,
        tenant_id=tenant_id,
        top_k=semantic_k,
        access_level=access_level,
        departments=departments,
    )
    keyword_results = await keyword_search(
        session,
        query=query,
        tenant_id=tenant_id,
        top_k=keyword_k,
        access_level=access_level,
        departments=departments,
    )

    return reciprocal_rank_fusion(semantic_results, keyword_results, top_k=top_k)
