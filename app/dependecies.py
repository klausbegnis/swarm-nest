"""
File: dependecies.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db.session import session_context
from app.services.database_service import DatabaseService


def get_dependency(request: Request) -> Any:
    """
    Get dependency.

    Args:
        request: FastAPI Request object (injected by dependency system).

    Returns:
        Any: The dependency.
    """
    # return request.app.state.dependency
    return None


def get_db() -> Generator[Session]:
    """Provide a session per request using the context manager."""
    with session_context() as db:
        yield db


def get_database_service(
    db: Annotated[Session, Depends(get_db)],
) -> DatabaseService:
    """Provides DatabaseService with the request session."""
    return DatabaseService(db)


DatabaseServiceDep = Annotated[DatabaseService, Depends(get_database_service)]
