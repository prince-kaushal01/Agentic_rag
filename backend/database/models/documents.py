from sqlalchemy import String, Integer, Text, Float, Boolean, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector
from backend.database.models.base import BaseModel
import uuid
import enum


class AccessLevel(str, enum.Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"


class DocumentStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    indexed = "indexed"
    failed = "failed"


class Document(BaseModel):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf, docx, md, csv
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    access_level: Mapped[AccessLevel] = mapped_column(
        SAEnum(AccessLevel), default=AccessLevel.internal
    )
    status: Mapped[DocumentStatus] = mapped_column(
        SAEnum(DocumentStatus), default=DocumentStatus.pending
    )
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    doc_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="documents")
    chunks: Mapped[list["DocumentChunk"]] = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)

    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section: Mapped[str | None] = mapped_column(String(500), nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    chunk_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
