"""
File: tool.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin


class Tool(Base, TimestampMixin):
    """
    Tool entity for functions that agents can use.

    Attributes:
        id: Primary key.
        name: Tool name (unique).
        definition: JSON schema (parameters, description).
        code_ref: Optional Python callable reference (e.g. module.func).
    """

    __tablename__ = "tools"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    definition: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    code_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
