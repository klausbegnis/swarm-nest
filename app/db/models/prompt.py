"""
File: prompt.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.agent import Agent


class Prompt(Base, TimestampMixin):
    """
    Prompt entity for templates assignable to agents.

    Attributes:
        id: Primary key.
        name: Human-readable prompt name.
        content: Template text (may contain variables).
        variables: List of variable names (e.g. ["user_name", "context"]).
    """

    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)

    agents: Mapped[list[Agent]] = relationship(
        "Agent",
        back_populates="prompt",
    )
