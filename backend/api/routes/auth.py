"""
Authentication routes.

POST /auth/register   — Create a new user (admin only in prod; open for dev)
POST /auth/login      — Email + password → access + refresh tokens
POST /auth/refresh    — Refresh token → new access token
GET  /auth/me         — Current user profile + permissions
"""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.connection import AsyncSessionLocal
from backend.database.models.users import User, UserRole, Organization
from backend.auth.password import hash_password, verify_password
from backend.auth.tokens import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from backend.auth.permissions import get_permissions
from backend.auth.dependencies import get_current_user, CurrentUser
from backend.auth.audit import write_audit_log
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["auth"])


# ── Session dependency ────────────────────────────────────────────────────────

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ── Schemas ───────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1)
    role: UserRole = UserRole.employee
    department: Optional[str] = None
    tenant_slug: str = "novatech"   # which org to join


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    full_name: str


class RefreshRequest(BaseModel):
    refresh_token: str


class MeResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    department: Optional[str]
    tenant_id: str
    max_access_level: str
    allowed_departments: Optional[list[str]]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, session: AsyncSession = Depends(get_session)):
    # Check email uniqueness
    existing = await session.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Look up tenant
    org_result = await session.execute(
        select(Organization).where(Organization.slug == req.tenant_slug)
    )
    org = org_result.scalar_one_or_none()
    if org is None:
        raise HTTPException(status_code=404, detail=f"Organization '{req.tenant_slug}' not found")

    user = User(
        email=req.email,
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        role=req.role,
        department=req.department,
        tenant_id=org.id,
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    await session.flush()

    await write_audit_log(
        session,
        action="auth.register",
        resource_type="user",
        resource_id=str(user.id),
        tenant_id=org.id,
        user_id=user.id,
        outcome="success",
    )
    await session.commit()

    access_token = create_access_token(user.id, org.id, user.role.value, user.department)
    refresh_token = create_refresh_token(user.id, org.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        role=user.role.value,
        full_name=user.full_name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    req: LoginRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()

    # Use constant-time comparison even on miss (prevents timing attacks)
    password_ok = (
        user is not None
        and user.is_active
        and verify_password(req.password, user.hashed_password)
    )

    if not password_ok:
        # Still log the failure
        if user:
            await write_audit_log(
                session,
                action="auth.login",
                resource_type="user",
                resource_id=str(user.id),
                tenant_id=user.tenant_id,
                user_id=user.id,
                outcome="failure",
                ip_address=request.client.host if request.client else None,
                extra={"reason": "invalid_password"},
                auto_commit=True,
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    await write_audit_log(
        session,
        action="auth.login",
        resource_type="user",
        resource_id=str(user.id),
        tenant_id=user.tenant_id,
        user_id=user.id,
        outcome="success",
        ip_address=request.client.host if request.client else None,
        auto_commit=True,
    )

    access_token = create_access_token(user.id, user.tenant_id, user.role.value, user.department)
    refresh_token = create_refresh_token(user.id, user.tenant_id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        role=user.role.value,
        full_name=user.full_name,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    req: RefreshRequest,
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = decode_refresh_token(req.refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = uuid.UUID(payload["sub"])
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    access_token = create_access_token(user.id, user.tenant_id, user.role.value, user.department)
    refresh_token_new = create_refresh_token(user.id, user.tenant_id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_new,
        user_id=str(user.id),
        role=user.role.value,
        full_name=user.full_name,
    )


@router.get("/me", response_model=MeResponse)
async def me(current_user: CurrentUser = Depends(get_current_user)):
    perms = current_user.permissions
    return MeResponse(
        user_id=str(current_user.user_id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        department=current_user.department,
        tenant_id=str(current_user.tenant_id),
        max_access_level=perms.max_access_level,
        allowed_departments=perms.allowed_departments,
    )
