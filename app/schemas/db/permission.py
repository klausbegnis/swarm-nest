"""
File: permission.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from app.schemas.db.base import DBBaseSchema, TimestampSchema


class PermissionBase(DBBaseSchema):
    """Shared fields for Permission."""

    name: str
    resource: str
    action: str


class PermissionCreate(PermissionBase):
    """Schema for creating a permission."""

    pass


class PermissionRead(PermissionBase, TimestampSchema):
    """Schema for reading a permission."""

    id: int
