from sqlalchemy import String, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.database.models.base import BaseModel
import uuid
import enum


class UserRole(str, enum.Enum):
    employee = "employee"
    engineer = "engineer"
    account_manager = "account_manager"
    manager = "manager"
    hr = "hr"
    admin = "admin"


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="organization")
    documents: Mapped[list] = relationship("Document", back_populates="organization")


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.employee)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )

    organization: Mapped["Organization"] = relationship("Organization", back_populates="users")
    conversations: Mapped[list] = relationship("Conversation", back_populates="user")
    audit_logs: Mapped[list] = relationship("AuditLog", back_populates="user")
    approvals: Mapped[list] = relationship(
        "Approval",
        foreign_keys="Approval.reviewed_by",
        back_populates="reviewed_by_user",
    )
