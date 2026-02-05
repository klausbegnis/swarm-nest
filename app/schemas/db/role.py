"""
File: role.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from app.schemas.db.base import DBBaseSchema, TimestampSchema


class RoleBase(DBBaseSchema):
    """Shared fields for Role."""

    name: str
    description: str | None = None


class RoleCreate(RoleBase):
    """Schema for creating a role."""

    pass


class RoleUpdate(DBBaseSchema):
    """Schema for partial role update."""

    name: str | None = None
    description: str | None = None


class RoleRead(RoleBase, TimestampSchema):
    """Schema for reading a role."""

    id: int
