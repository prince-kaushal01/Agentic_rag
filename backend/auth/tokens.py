"""
JWT access + refresh token creation and verification.

Access token  — short-lived (60 min), used on every request
Refresh token — long-lived (7 days), used only to get a new access token

Token payload (claims):
    sub         user UUID (string)
    tenant_id   organization UUID (string)
    role        UserRole value
    department  optional string
    exp         expiry timestamp
    type        "access" | "refresh"
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

_SECRET = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
_ALGORITHM = "HS256"
_ACCESS_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
_REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def _make_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    payload = data.copy()
    payload.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "iat": datetime.now(timezone.utc),
            "type": token_type,
        }
    )
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


def create_access_token(
    user_id: uuid.UUID,
    tenant_id: uuid.UUID,
    role: str,
    department: str | None = None,
) -> str:
    return _make_token(
        {
            "sub": str(user_id),
            "tenant_id": str(tenant_id),
            "role": role,
            "department": department,
        },
        timedelta(minutes=_ACCESS_EXPIRE_MIN),
        "access",
    )


def create_refresh_token(user_id: uuid.UUID, tenant_id: uuid.UUID) -> str:
    return _make_token(
        {"sub": str(user_id), "tenant_id": str(tenant_id)},
        timedelta(days=_REFRESH_EXPIRE_DAYS),
        "refresh",
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate an access token.
    Raises JWTError on invalid/expired tokens.
    """
    payload = jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    if payload.get("type") != "access":
        raise JWTError("Not an access token")
    return payload


def decode_refresh_token(token: str) -> dict:
    payload = jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    if payload.get("type") != "refresh":
        raise JWTError("Not a refresh token")
    return payload
