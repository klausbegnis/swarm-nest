"""
File: prompt.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from app.schemas.db.base import DBBaseSchema, TimestampSchema


class PromptBase(DBBaseSchema):
    """Shared fields for Prompt."""

    name: str
    content: str
    variables: list[str] | None = None


class PromptCreate(PromptBase):
    """Schema for creating a prompt."""

    pass


class PromptUpdate(DBBaseSchema):
    """Schema for partial prompt update."""

    name: str | None = None
    content: str | None = None
    variables: list[str] | None = None


class PromptRead(PromptBase, TimestampSchema):
    """Schema for reading a prompt."""

    id: int
