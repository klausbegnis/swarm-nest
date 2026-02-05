"""
File: agent.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.prompt import Prompt


class Agent(Base, TimestampMixin):
    """
    Agent entity for LangChain/LangGraph agent definitions.

    Attributes:
        id: Primary key.
        name: Human-readable agent name.
        config: JSON config (model, etc.).
        prompt_id: Optional FK to the single prompt assigned to this agent.
    """

    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    prompt_id: Mapped[int | None] = mapped_column(
        ForeignKey("prompts.id", ondelete="SET NULL"),
        nullable=True,
    )

    prompt: Mapped[Prompt | None] = relationship(
        "Prompt",
        back_populates="agents",
    )
