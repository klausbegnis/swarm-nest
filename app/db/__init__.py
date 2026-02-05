"""
File: __init__.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from app.db.base import Base
from app.db.session import engine, session_context, SessionLocal

# Import models so Base.metadata is populated (for create_all).
from app.db import models as _models  # noqa: F401

__all__ = [
    "Base",
    "engine",
    "session_context",
    "SessionLocal",
]
