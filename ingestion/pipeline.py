"""
Main ingestion pipeline.

Usage:
    asyncio.run(run_pipeline(path, department, tenant_id))

Flow:
    File → Parser → Chunker → Embedder → pgvector index
"""
import uuid
from pathlib import Path
from dataclasses import dataclass

from backend.database.connection import AsyncSessionLocal
from ingestion.parsers.registry import parse_file
from ingestion.chunking.chunker import chunk_document
from ingestion.embeddings.embedder import embed_chunks
from ingestion.indexing.pgvector_index import upsert_document, index_chunks


@dataclass
class IngestionResult:
    document_id: str
    file_name: str
    chunks_indexed: int
    status: str
    error: str | None = None


async def run_pipeline(
    file_path: str | Path,
    *,
    department: str,
    tenant_id: uuid.UUID,
    access_level: str = "internal",
    uploaded_by: uuid.UUID | None = None,
) -> IngestionResult:
    path = Path(file_path)

    # 1. Parse
    print(f"  [parse]  {path.name}")
    parsed = parse_file(path)

    # 2. Chunk
    print(f"  [chunk]  {path.name}")
    chunks = chunk_document(parsed)
    if not chunks:
        return IngestionResult(
            document_id="",
            file_name=path.name,
            chunks_indexed=0,
            status="failed",
            error="No chunks produced",
        )

    # 3. Embed
    print(f"  [embed]  {path.name}  ({len(chunks)} chunks)")
    embeddings = embed_chunks(chunks)

    # 4. Index
    async with AsyncSessionLocal() as session:
        doc = await upsert_document(
            session,
            title=parsed.title,
            file_name=parsed.file_name,
            file_type=parsed.file_type,
            department=department,
            access_level=access_level,
            tenant_id=tenant_id,
            uploaded_by=uploaded_by,
            doc_metadata=parsed.metadata,
        )
        count = await index_chunks(session, document=doc, chunks=chunks, embeddings=embeddings)

    print(f"  [done]   {path.name}  → {count} chunks indexed")
    return IngestionResult(
        document_id=str(doc.id),
        file_name=path.name,
        chunks_indexed=count,
        status="indexed",
    )
