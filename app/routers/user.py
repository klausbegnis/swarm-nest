"""
File: user.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi import APIRouter, status
from pydantic import BaseModel

from app.core.exceptions import NotFoundException
from app.dependecies import DatabaseServiceDep
from app.schemas.api.base import SuccessResponse
from app.schemas.db.base import orm_to_schema
from app.schemas.db.role import RoleRead
from app.schemas.db.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["user"])


class UserRoleAssign(BaseModel):
    """Body for assigning a role to a user."""

    role_id: int


@router.post(
    "/",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[UserRead]:
    """
    Create a new user (password is hashed before storage).

    Args:
        data: Email, username, full_name, password, is_active.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the created user (UserRead, no password).
    """
    user = db_service.create_user(data)
    return SuccessResponse(
        message="User created",
        data=orm_to_schema(user, UserRead),
    )


@router.get("/{user_id}/roles", response_model=SuccessResponse[list[RoleRead]])
def list_user_roles(
    user_id: int,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[list[RoleRead]]:
    """
    List all roles assigned to a user.

    Args:
        user_id: User primary key.
        db_service: Injected database service.

    Returns:
        SuccessResponse with list of roles.

    Raises:
        NotFoundException: If user not found.
    """
    if db_service.get_user(user_id) is None:
        raise NotFoundException(detail="User not found")
    roles = db_service.list_roles_for_user(user_id)
    return SuccessResponse(
        message="User roles listed",
        data=[orm_to_schema(r, RoleRead) for r in roles],
    )


@router.post(
    "/{user_id}/roles",
    response_model=SuccessResponse[RoleRead],
    status_code=status.HTTP_201_CREATED,
)
def assign_role_to_user(
    user_id: int,
    data: UserRoleAssign,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[RoleRead]:
    """
    Assign a role to a user (idempotent).

    Args:
        user_id: User primary key.
        data: role_id to assign.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the assigned role.

    Raises:
        NotFoundException: If user or role not found.
    """
    if db_service.get_user(user_id) is None:
        raise NotFoundException(detail="User not found")
    role = db_service.get_role(data.role_id)
    if role is None:
        raise NotFoundException(detail="Role not found")
    db_service.assign_role_to_user(user_id, data.role_id)
    return SuccessResponse(
        message="Role assigned",
        data=orm_to_schema(role, RoleRead),
    )


@router.delete(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_role_from_user(
    user_id: int,
    role_id: int,
    db_service: DatabaseServiceDep,
) -> None:
    """
    Remove a role from a user.

    Args:
        user_id: User primary key.
        role_id: Role primary key.
        db_service: Injected database service.

    Raises:
        NotFoundException: If user not found or role was not assigned.
    """
    if db_service.get_user(user_id) is None:
        raise NotFoundException(detail="User not found")
    removed = db_service.remove_role_from_user(user_id, role_id)
    if not removed:
        raise NotFoundException(
            detail="Role not found or was not assigned to user"
        )
