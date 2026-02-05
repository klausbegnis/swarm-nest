"""
File: prompt.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi import APIRouter, Query, status

from app.core.exceptions import NotFoundException
from app.dependecies import DatabaseServiceDep
from app.schemas.api.base import SuccessResponse
from app.schemas.db.base import orm_to_schema
from app.schemas.db.prompt import PromptCreate, PromptRead, PromptUpdate

router = APIRouter(prefix="/prompts", tags=["prompt"])


@router.post(
    "/",
    response_model=SuccessResponse[PromptRead],
    status_code=status.HTTP_201_CREATED,
)
def create_prompt(
    data: PromptCreate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[PromptRead]:
    """
    Create a new prompt.

    Args:
        data: Prompt name, content, and optional variables.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the created prompt (PromptRead).
    """
    prompt = db_service.create_prompt(data)
    return SuccessResponse(
        message="Prompt created",
        data=orm_to_schema(prompt, PromptRead),
    )


@router.get("/", response_model=SuccessResponse[list[PromptRead]])
def list_prompts(
    db_service: DatabaseServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> SuccessResponse[list[PromptRead]]:
    """
    List prompts with optional pagination.

    Args:
        db_service: Injected database service.
        skip: Number of records to skip.
        limit: Max records to return.

    Returns:
        SuccessResponse with list of prompts.
    """
    prompts = db_service.list_prompts(skip=skip, limit=limit)
    return SuccessResponse(
        message="Prompts listed",
        data=[orm_to_schema(p, PromptRead) for p in prompts],
    )


@router.get("/{id}", response_model=SuccessResponse[PromptRead])
def get_prompt(
    id: int,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[PromptRead]:
    """
    Get a prompt by id.

    Args:
        id: Prompt primary key.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the prompt.

    Raises:
        NotFoundException: If prompt not found.
    """
    prompt = db_service.get_prompt(id)
    if prompt is None:
        raise NotFoundException(detail="Prompt not found")
    return SuccessResponse(
        message="Prompt found",
        data=orm_to_schema(prompt, PromptRead),
    )


@router.patch("/{id}", response_model=SuccessResponse[PromptRead])
def update_prompt(
    id: int,
    data: PromptUpdate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[PromptRead]:
    """
    Update a prompt by id (partial update).

    Args:
        id: Prompt primary key.
        data: Fields to update.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the updated prompt.

    Raises:
        NotFoundException: If prompt not found.
    """
    prompt = db_service.update_prompt(id, data)
    if prompt is None:
        raise NotFoundException(detail="Prompt not found")
    return SuccessResponse(
        message="Prompt updated",
        data=orm_to_schema(prompt, PromptRead),
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prompt(
    id: int,
    db_service: DatabaseServiceDep,
) -> None:
    """
    Delete a prompt by id.

    Args:
        id: Prompt primary key.
        db_service: Injected database service.

    Raises:
        NotFoundException: If prompt not found.
    """
    deleted = db_service.delete_prompt(id)
    if not deleted:
        raise NotFoundException(detail="Prompt not found")
