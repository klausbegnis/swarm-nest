"""
File: agent.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from typing import Any

from pydantic import Field

from app.schemas.db.base import DBBaseSchema, TimestampSchema


class AgentBase(DBBaseSchema):
    """Shared fields for Agent."""

    name: str
    config: dict[str, Any] = Field(default_factory=dict)
    prompt_id: int | None = None


class AgentCreate(AgentBase):
    """Schema for creating an agent."""

    pass


class AgentUpdate(DBBaseSchema):
    """Schema for partial agent update."""

    name: str | None = None
    config: dict[str, Any] | None = None
    prompt_id: int | None = None


class AgentRead(AgentBase, TimestampSchema):
    """Schema for reading an agent."""

    id: int
