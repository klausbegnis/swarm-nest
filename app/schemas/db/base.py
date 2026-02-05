"""
File: base.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DBBaseSchema(BaseModel):
    """
    Base Pydantic schema for database entities.

    Disables ORM mode by default; subclasses enable it for Read schemas
    when needed. Uses non-negative integers for ids.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="forbid",
    )


class TimestampSchema(BaseModel):
    """Mixin fields for created_at and updated_at."""

    created_at: datetime
    updated_at: datetime


def orm_to_schema[T: BaseModel](orm_instance: Any, schema_class: type[T]) -> T:
    """Build a Pydantic schema from an ORM instance by reading each field.

    Ensures DB values (e.g. id, timestamps) are captured at read time and
    not lost when the session closes or the object is expired.

    Args:
        orm_instance: SQLAlchemy model instance.
        schema_class: Pydantic Read schema class (e.g. AgentRead).

    Returns:
        Instance of schema_class with values from orm_instance.
    """
    data = {
        name: getattr(orm_instance, name)
        for name in schema_class.model_fields
    }
    return schema_class.model_validate(data)
