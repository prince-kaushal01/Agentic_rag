"""
Cross-encoder reranker.

Takes a list of candidate chunks and re-scores them using a cross-encoder
(query + document) model, which is more accurate than bi-encoder similarity
but too slow to run over the full corpus — run it on a small candidate set (≤20).

Model: cross-encoder/ms-marco-MiniLM-L-6-v2  (~70MB, fast, strong performance)
"""
from __future__ import annotations

from sentence_transformers import CrossEncoder

from backend.retrieval.semantic import RetrievedChunk

_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_reranker: CrossEncoder | None = None


def _get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(_MODEL_NAME, max_length=512)
    return _reranker


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    top_k: int = 6,
) -> list[RetrievedChunk]:
    """
    Re-score chunks using the cross-encoder and return top_k.
    Input chunks are typically the output of hybrid_search (≤20 candidates).
    """
    if not chunks:
        return []

    reranker = _get_reranker()

    # Build (query, passage) pairs
    pairs = [(query, chunk.content) for chunk in chunks]
    scores = reranker.predict(pairs)

    # Pair score with chunk and sort
    scored = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)

    results = []
    for score, chunk in scored[:top_k]:
        results.append(
            RetrievedChunk(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                content=chunk.content,
                score=float(score),      # cross-encoder logit score
                page_number=chunk.page_number,
                section=chunk.section,
                department=chunk.department,
                access_level=chunk.access_level,
                file_name=chunk.file_name,
            )
        )

    return results
