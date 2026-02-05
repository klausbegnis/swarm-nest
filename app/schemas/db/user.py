"""
File: user.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from app.schemas.db.base import DBBaseSchema, TimestampSchema


class UserBase(DBBaseSchema):
    """Shared fields for User."""

    email: str
    username: str
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a user (includes plain password)."""

    password: str


class UserUpdate(DBBaseSchema):
    """Schema for partial user update."""

    email: str | None = None
    username: str | None = None
    full_name: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserRead(UserBase, TimestampSchema):
    """Schema for reading a user (excludes password)."""

    id: int
