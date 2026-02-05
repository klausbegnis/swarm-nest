"""
File: role.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi import APIRouter, Query, status

from app.core.exceptions import NotFoundException
from app.dependecies import DatabaseServiceDep
from app.schemas.api.base import SuccessResponse
from app.schemas.db.role import RoleCreate, RoleRead, RoleUpdate
from app.schemas.db.base import orm_to_schema

router = APIRouter(prefix="/roles", tags=["role"])


@router.post(
    "/",
    response_model=SuccessResponse[RoleRead],
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    data: RoleCreate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[RoleRead]:
    """
    Create a new role.

    Args:
        data: Role name and optional description.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the created role (RoleRead).
    """
    role = db_service.create_role(data)
    return SuccessResponse(
        message="Role created",
        data=orm_to_schema(role, RoleRead),
    )


@router.get("/", response_model=SuccessResponse[list[RoleRead]])
def list_roles(
    db_service: DatabaseServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> SuccessResponse[list[RoleRead]]:
    """
    List roles with optional pagination.

    Args:
        db_service: Injected database service.
        skip: Number of records to skip.
        limit: Max records to return.

    Returns:
        SuccessResponse with list of roles.
    """
    roles = db_service.list_roles(skip=skip, limit=limit)
    return SuccessResponse(
        message="Roles listed",
        data=[orm_to_schema(r, RoleRead) for r in roles],
    )


@router.get("/{id}", response_model=SuccessResponse[RoleRead])
def get_role(
    id: int,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[RoleRead]:
    """
    Get a role by id.

    Args:
        id: Role primary key.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the role.

    Raises:
        NotFoundException: If role not found.
    """
    role = db_service.get_role(id)
    if role is None:
        raise NotFoundException(detail="Role not found")
    return SuccessResponse(
        message="Role found",
        data=orm_to_schema(role, RoleRead),
    )


@router.patch("/{id}", response_model=SuccessResponse[RoleRead])
def update_role(
    id: int,
    data: RoleUpdate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[RoleRead]:
    """
    Update a role by id (partial update).

    Args:
        id: Role primary key.
        data: Fields to update.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the updated role.

    Raises:
        NotFoundException: If role not found.
    """
    role = db_service.update_role(id, data)
    if role is None:
        raise NotFoundException(detail="Role not found")
    return SuccessResponse(
        message="Role updated",
        data=orm_to_schema(role, RoleRead),
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    id: int,
    db_service: DatabaseServiceDep,
) -> None:
    """
    Delete a role by id.

    Args:
        id: Role primary key.
        db_service: Injected database service.

    Raises:
        NotFoundException: If role not found.
    """
    deleted = db_service.delete_role(id)
    if not deleted:
        raise NotFoundException(detail="Role not found")
