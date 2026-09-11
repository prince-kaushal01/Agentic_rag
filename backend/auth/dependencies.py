"""
FastAPI dependency: get_current_user

Extracts and validates the JWT from the Authorization header,
loads the User from DB, and returns a CurrentUser dataclass
that carries identity + permissions for use in route handlers.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.tokens import decode_access_token
from backend.auth.permissions import get_permissions, RolePermissions
from backend.database.connection import AsyncSessionLocal
from backend.database.models.users import User

_bearer = HTTPBearer(auto_error=True)


@dataclass
class CurrentUser:
    user_id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    full_name: str
    role: str
    department: str | None
    permissions: RolePermissions


# ── DB session for auth ───────────────────────────────────────────────────────

async def _get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ── Main dependency ───────────────────────────────────────────────────────────

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(_bearer),
    session: AsyncSession = Depends(_get_session),
) -> CurrentUser:
    """
    Validate Bearer token → load User → return CurrentUser.
    Raises 401 on any auth failure.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(creds.credentials)
    except JWTError:
        raise credentials_error

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise credentials_error

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_error

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_error

    return CurrentUser(
        user_id=user.id,
        tenant_id=user.tenant_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        department=user.department,
        permissions=get_permissions(user.role.value),
    )


def require_role(*roles: str):
    """
    Dependency factory: enforce that the current user has one of the given roles.

    Usage:
        @router.get("/admin-only")
        async def view(user: CurrentUser = Depends(require_role("admin", "manager"))):
            ...
    """
    async def _check(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted for this action",
            )
        return current_user
    return _check
