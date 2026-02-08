"""
File: tool.py
Project: swarm-nest
Created: Sunday, 8th February 2026 6:06:39 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from fastapi import APIRouter
from langchain.tools import Tool

from app.dependecies import ToolProviderDep
from app.schemas.api.base import SuccessResponse

router = APIRouter(prefix="/tools", tags=["tool"])


@router.get("/", response_model=SuccessResponse[list[Tool]])
def get_tools(tool_provider: ToolProviderDep) -> list[Tool]:
    """
    Get all tools.

    Args:
        tool_provider: Injected tool provider.

    Returns:
        list[Tool]: All tools.
    """
    return SuccessResponse(
        message="Tools listed",
        data=tool_provider.get_tools(),
    )
