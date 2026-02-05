"""
File: dependecies.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from typing import Any

from fastapi import Request


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
