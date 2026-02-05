"""
File: agent.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi import APIRouter, Query, status

from app.core.exceptions import NotFoundException
from app.dependecies import DatabaseServiceDep
from app.schemas.api.base import SuccessResponse
from app.schemas.db.agent import AgentCreate, AgentRead, AgentUpdate
from app.schemas.db.base import orm_to_schema

router = APIRouter(prefix="/agents", tags=["agent"])


@router.post(
    "/",
    response_model=SuccessResponse[AgentRead],
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    data: AgentCreate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[AgentRead]:
    """
    Create a new agent.

    Args:
        data: Agent name, config, and optional prompt_id.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the created agent (AgentRead).
    """
    agent = db_service.create_agent(data)
    return SuccessResponse(
        message="Agent created",
        data=orm_to_schema(agent, AgentRead),
    )


@router.get("/", response_model=SuccessResponse[list[AgentRead]])
def list_agents(
    db_service: DatabaseServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> SuccessResponse[list[AgentRead]]:
    """
    List agents with optional pagination.

    Args:
        db_service: Injected database service.
        skip: Number of records to skip.
        limit: Max records to return.

    Returns:
        SuccessResponse with list of agents.
    """
    agents = db_service.list_agents(skip=skip, limit=limit)
    return SuccessResponse(
        message="Agents listed",
        data=[orm_to_schema(a, AgentRead) for a in agents],
    )


@router.get("/{id}", response_model=SuccessResponse[AgentRead])
def get_agent(
    id: int,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[AgentRead]:
    """
    Get an agent by id.

    Args:
        id: Agent primary key.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the agent.

    Raises:
        NotFoundException: If agent not found.
    """
    agent = db_service.get_agent(id)
    if agent is None:
        raise NotFoundException(detail="Agent not found")
    return SuccessResponse(
        message="Agent found",
        data=orm_to_schema(agent, AgentRead),
    )


@router.patch("/{id}", response_model=SuccessResponse[AgentRead])
def update_agent(
    id: int,
    data: AgentUpdate,
    db_service: DatabaseServiceDep,
) -> SuccessResponse[AgentRead]:
    """
    Update an agent by id (partial update).

    Args:
        id: Agent primary key.
        data: Fields to update.
        db_service: Injected database service.

    Returns:
        SuccessResponse with the updated agent.

    Raises:
        NotFoundException: If agent not found.
    """
    agent = db_service.update_agent(id, data)
    if agent is None:
        raise NotFoundException(detail="Agent not found")
    return SuccessResponse(
        message="Agent updated",
        data=orm_to_schema(agent, AgentRead),
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(
    id: int,
    db_service: DatabaseServiceDep,
) -> None:
    """
    Delete an agent by id.

    Args:
        id: Agent primary key.
        db_service: Injected database service.

    Raises:
        NotFoundException: If agent not found.
    """
    deleted = db_service.delete_agent(id)
    if not deleted:
        raise NotFoundException(detail="Agent not found")
