"""
File: dependecies.py
Project: replace with your project name
Created: Wednesday, 29th October 2025 4:27:29 pm
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
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
