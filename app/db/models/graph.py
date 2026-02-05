"""
File: graph.py
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


class Graph(Base, TimestampMixin):
    """
    Graph entity for LangGraph execution definitions.

    Attributes:
        id: Primary key.
        name: Human-readable graph name.
        definition: JSON graph structure (nodes, edges, state).
        entry_node: Name of the entry node for execution.
    """

    __tablename__ = "graphs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    definition: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    entry_node: Mapped[str] = mapped_column(String(255), nullable=False)
