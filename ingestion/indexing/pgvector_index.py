import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from backend.database.models.documents import Document, DocumentChunk, DocumentStatus, AccessLevel
from backend.database.models.users import Organization
from ingestion.chunking.chunker import Chunk


async def upsert_document(
    session: AsyncSession,
    *,
    title: str,
    file_name: str,
    file_type: str,
    department: str,
    access_level: str,
    tenant_id: uuid.UUID,
    uploaded_by: uuid.UUID | None = None,
    doc_metadata: dict | None = None,
) -> Document:
    """Create a Document record and mark it as processing."""
    doc = Document(
        title=title,
        file_name=file_name,
        file_type=file_type,
        department=department,
        access_level=AccessLevel(access_level),
        status=DocumentStatus.processing,
        tenant_id=tenant_id,
        uploaded_by=uploaded_by,
        doc_metadata=doc_metadata or {},
    )
    session.add(doc)
    await session.flush()   # get the id without committing
    return doc


async def index_chunks(
    session: AsyncSession,
    *,
    document: Document,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> int:
    """Persist all chunks with their embeddings. Returns count indexed."""
    # Remove any existing chunks for this document (re-index scenario)
    await session.execute(
        delete(DocumentChunk).where(DocumentChunk.document_id == document.id)
    )

    db_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        db_chunk = DocumentChunk(
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            embedding=embedding,
            page_number=chunk.page_number,
            section=chunk.section,
            token_count=chunk.token_count,
            chunk_metadata=chunk.metadata,
            document_id=document.id,
            tenant_id=document.tenant_id,
        )
        db_chunks.append(db_chunk)

    session.add_all(db_chunks)

    # Mark document as indexed
    document.status = DocumentStatus.indexed
    await session.commit()

    return len(db_chunks)
