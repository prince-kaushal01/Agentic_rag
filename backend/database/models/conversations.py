from sqlalchemy import String, Text, ForeignKey, Enum as SAEnum, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.database.models.base import BaseModel
import uuid
import enum


class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"


class Conversation(BaseModel):
    __tablename__ = "conversations"

    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="conversation")


class Message(BaseModel):
    __tablename__ = "messages"

    role: Mapped[MessageRole] = mapped_column(SAEnum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(nullable=True)
    cost_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sources: Mapped[list | None] = mapped_column(JSON, nullable=True)  # cited doc chunks
    msg_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
