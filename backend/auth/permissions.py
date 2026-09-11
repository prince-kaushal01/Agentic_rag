"""
RBAC permissions.

Maps each UserRole to:
  - max_access_level  : highest document access_level the role may read
  - allowed_departments: set of department names, or None = all non-restricted

Permission matrix (from DASHBOARD.md):
  Role         | public | internal | confidential | restricted | departments
  -------------|--------|----------|--------------|------------|------------------
  employee     |   ✅   |    ✅    |      ❌      |     ❌     | None (all internal)
  engineer     |   ✅   |    ✅    |      ❌      |     ❌     | engineering + sales + ops + marketing + support
  account_mgr  |   ✅   |    ✅    |      ❌      |     ❌     | sales + marketing + customer_support
  manager      |   ✅   |    ✅    |      ✅      |     ❌     | all confidential and below
  hr           |   ✅   |    ✅    |      ❌      |     ✅     | hr only (restricted)
  admin        |   ✅   |    ✅    |      ✅      |     ✅     | all
"""
from __future__ import annotations

from dataclasses import dataclass

from backend.database.models.users import UserRole


@dataclass(frozen=True)
class RolePermissions:
    max_access_level: str           # "public" | "internal" | "confidential" | "restricted"
    allowed_departments: list[str] | None  # None = no department filter


_ROLE_PERMISSIONS: dict[str, RolePermissions] = {
    UserRole.employee.value: RolePermissions(
        max_access_level="internal",
        allowed_departments=None,
    ),
    UserRole.engineer.value: RolePermissions(
        max_access_level="internal",
        allowed_departments=["engineering", "sales", "operations", "marketing", "customer_support"],
    ),
    UserRole.account_manager.value: RolePermissions(
        max_access_level="internal",
        allowed_departments=["sales", "marketing", "customer_support"],
    ),
    UserRole.manager.value: RolePermissions(
        max_access_level="confidential",
        allowed_departments=None,
    ),
    UserRole.hr.value: RolePermissions(
        max_access_level="restricted",
        allowed_departments=["hr"],
    ),
    UserRole.admin.value: RolePermissions(
        max_access_level="restricted",
        allowed_departments=None,
    ),
}


def get_permissions(role: str) -> RolePermissions:
    """Return permissions for a role. Defaults to employee if unknown."""
    return _ROLE_PERMISSIONS.get(role, _ROLE_PERMISSIONS[UserRole.employee.value])


def role_can_access_level(role: str, required_level: str) -> bool:
    """Check if a role can access a given access_level document."""
    order = ["public", "internal", "confidential", "restricted"]
    perms = get_permissions(role)
    try:
        return order.index(perms.max_access_level) >= order.index(required_level)
    except ValueError:
        return False
