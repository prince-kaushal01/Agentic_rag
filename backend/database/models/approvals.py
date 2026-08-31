from sqlalchemy import String, Text, ForeignKey, Enum as SAEnum, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.database.models.base import BaseModel
import uuid
import enum


class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    edited_and_approved = "edited_and_approved"


class Approval(BaseModel):
    __tablename__ = "approvals"

    action_type: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. send_email
    action_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # draft content
    edited_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # if user edited
    status: Mapped[ApprovalStatus] = mapped_column(
        SAEnum(ApprovalStatus), default=ApprovalStatus.pending
    )
    review_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    requested_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    task: Mapped["Task"] = relationship("Task", back_populates="approvals")
    reviewed_by_user: Mapped["User"] = relationship(
        "User", foreign_keys=[reviewed_by], back_populates="approvals"
    )
