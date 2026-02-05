"""
File: __init__.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from .agent import router as agent_router
from .health import router as health_router
from .prompt import router as prompt_router
from .role import router as role_router
from .user import router as user_router

__all__ = [
    "agent_router",
    "health_router",
    "prompt_router",
    "role_router",
    "user_router",
]
