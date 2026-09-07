"""
POST /chat  — Production RAG chat endpoint.

Pipeline: query rewrite → hybrid search (semantic + BM25 + RRF) → cross-encoder rerank
          → context build → LLM answer → persist + return

Request body:
    query           str         User question
    conversation_id str | null  Existing conversation UUID (null = new)
    tenant_id       str         Organization UUID
    user_id         str         User UUID
    access_level    str         Caller's max access level (public/internal/confidential/restricted)
    departments     list[str]   Optional department filter (null = all permitted)
    top_k           int         Final chunks sent to LLM (default 6)
    retrieval_mode  str         "hybrid" (default) | "semantic" | "keyword"
    rerank          bool        Whether to apply cross-encoder reranking (default True)

Response:
    answer          str         LLM-generated answer with [N] citations
    sources         list        Cited document metadata
    conversation_id str         UUID of conversation (new or existing)
    retrieval_mode  str         Mode actually used
    rewritten_query str | null  Rewritten query if different from original
    tokens_used     dict        input / output token counts
    cost_usd        float       Estimated LLM cost for this turn
    model           str         Model ID used
"""
from __future__ import annotations

import asyncio
import logging
import traceback
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database.connection import AsyncSessionLocal
from backend.database.models.conversations import Conversation, Message, MessageRole
from backend.retrieval.semantic import semantic_search
from backend.retrieval.keyword import keyword_search
from backend.retrieval.hybrid import hybrid_search
from backend.retrieval.reranker import rerank
from backend.retrieval.query_rewriter import rewrite_query
from backend.retrieval.context_builder import build_context
from backend.retrieval.llm import answer_with_context

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    tenant_id: str
    user_id: str
    access_level: str = "internal"
    departments: Optional[list[str]] = None
    top_k: int = Field(default=6, ge=1, le=20)
    retrieval_mode: str = Field(default="hybrid", pattern="^(hybrid|semantic|keyword)$")
    use_rerank: bool = True


class SourceOut(BaseModel):
    chunk_id: str
    document_id: str
    file_name: str
    department: Optional[str]
    section: Optional[str]
    page_number: Optional[int]
    relevance_score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceOut]
    conversation_id: str
    retrieval_mode: str
    rewritten_query: Optional[str]
    tokens_used: dict
    cost_usd: float
    model: str


# ── DB session dependency ─────────────────────────────────────────────────────

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _get_or_create_conversation(
    session: AsyncSession,
    conversation_id: str | None,
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    title: str,
) -> Conversation:
    if conversation_id:
        result = await session.execute(
            select(Conversation).where(Conversation.id == uuid.UUID(conversation_id))
        )
        conv = result.scalar_one_or_none()
        if conv is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conv

    conv = Conversation(title=title[:100], tenant_id=tenant_id, user_id=user_id)
    session.add(conv)
    await session.flush()
    return conv


async def _load_history(session: AsyncSession, conversation_id: uuid.UUID) -> list[dict]:
    """Load last 10 turns (20 messages) for multi-turn context."""
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.role.in_([MessageRole.user, MessageRole.assistant]))
        .order_by(Message.created_at.desc())
        .limit(20)
    )
    messages = list(reversed(result.scalars().all()))
    return [{"role": m.role.value, "content": m.content} for m in messages]


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, session: AsyncSession = Depends(get_session)):
    try:
        return await _chat_impl(req, session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Chat error: %s\n%s", e, traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


async def _chat_impl(req: ChatRequest, session: AsyncSession) -> ChatResponse:
    tenant_id = uuid.UUID(req.tenant_id)
    user_id = uuid.UUID(req.user_id)

    # 1. Get or create conversation
    conv = await _get_or_create_conversation(
        session, req.conversation_id, tenant_id, user_id, title=req.query[:80]
    )

    # 2. Load conversation history
    history = await _load_history(session, conv.id)

    # 3. Query rewriting — make query standalone if it references prior context
    rewritten = await asyncio.to_thread(rewrite_query, req.query, history)
    search_query = rewritten if rewritten != req.query else req.query
    rewritten_display = rewritten if rewritten != req.query else None

    # 4. Retrieval — wider candidate set before reranking
    candidate_k = min(req.top_k * 3, 20)   # fetch 3x, rerank down to top_k

    retrieval_kwargs = dict(
        session=session,
        query=search_query,
        tenant_id=tenant_id,
        access_level=req.access_level,
        departments=req.departments,
    )

    if req.retrieval_mode == "hybrid":
        candidates = await hybrid_search(
            **retrieval_kwargs,
            top_k=candidate_k,
            semantic_k=candidate_k,
            keyword_k=candidate_k,
        )
    elif req.retrieval_mode == "semantic":
        candidates = await semantic_search(**retrieval_kwargs, top_k=candidate_k)
    else:
        candidates = await keyword_search(**retrieval_kwargs, top_k=candidate_k)

    # 5. Cross-encoder reranking
    if req.use_rerank and candidates:
        chunks = await asyncio.to_thread(rerank, search_query, candidates, req.top_k)
    else:
        chunks = candidates[: req.top_k]

    # 6. Build context block
    context = build_context(chunks)

    # 7. LLM answer (in thread — blocking I/O)
    llm_resp = await asyncio.to_thread(
        answer_with_context, req.query, context, history
    )

    # 8. Map cited indices → sources
    cited_sources = []
    for idx in llm_resp.cited_indices:
        if 1 <= idx <= len(context.sources):
            src = context.sources[idx - 1]
            cited_sources.append(
                SourceOut(
                    chunk_id=src.chunk_id,
                    document_id=src.document_id,
                    file_name=src.file_name,
                    department=src.department,
                    section=src.section,
                    page_number=src.page_number,
                    relevance_score=round(src.score, 4),
                )
            )

    # Fallback: if LLM cited nothing, surface all retrieved sources
    if not cited_sources:
        cited_sources = [
            SourceOut(
                chunk_id=src.chunk_id,
                document_id=src.document_id,
                file_name=src.file_name,
                department=src.department,
                section=src.section,
                page_number=src.page_number,
                relevance_score=round(src.score, 4),
            )
            for src in context.sources
        ]

    # 9. Persist both messages
    session.add(Message(
        role=MessageRole.user,
        content=req.query,
        conversation_id=conv.id,
        tenant_id=tenant_id,
    ))
    session.add(Message(
        role=MessageRole.assistant,
        content=llm_resp.answer,
        token_count=llm_resp.input_tokens + llm_resp.output_tokens,
        cost_usd=llm_resp.cost_usd,
        model_used=llm_resp.model,
        sources=[
            {
                "chunk_id": s.chunk_id,
                "file_name": s.file_name,
                "department": s.department,
                "section": s.section,
                "page_number": s.page_number,
                "score": s.relevance_score,
            }
            for s in cited_sources
        ],
        conversation_id=conv.id,
        tenant_id=tenant_id,
    ))
    await session.commit()

    return ChatResponse(
        answer=llm_resp.answer,
        sources=cited_sources,
        conversation_id=str(conv.id),
        retrieval_mode=req.retrieval_mode,
        rewritten_query=rewritten_display,
        tokens_used={
            "input": llm_resp.input_tokens,
            "output": llm_resp.output_tokens,
            "total": llm_resp.input_tokens + llm_resp.output_tokens,
        },
        cost_usd=llm_resp.cost_usd,
        model=llm_resp.model,
    )
