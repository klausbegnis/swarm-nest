"""
File: tool_provider.py
Project: swarm-nest
Created: Sunday, 8th February 2026 6:04:49 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from langchain.tools import BaseTool

from app.core.logger import get_logger
from app.tools import tools as tools_list

logger = get_logger(__name__)


class ToolProvider:
    """
    Provider for tools.
    """

    def __init__(self) -> None:
        """
        Initialize the ToolProvider.
        """
        self._tools = self._get_tools()

    def _get_tools(self) -> dict[str, BaseTool]:
        """
        Build a name -> tool map (one tool per name).

        Returns:
            dict[str, BaseTool]: Tool name to BaseTool instance.
        """
        tools: dict[str, BaseTool] = {}
        # first ensure only one tool with the same name
        for tool in tools_list:
            if tool.name in tools:
                logger.warning(
                    f"Multiple tools with the same name found: {tool.name}"
                )
                continue
            tools[tool.name] = tool
        return tools

    @property
    def tools(self) -> dict[str, BaseTool]:
        """
        Get the tools (name -> BaseTool).
        """
        return self._tools

    def get_tool(self, tool_name: str) -> BaseTool:
        """
        Get a tool by name.

        Raises:
            KeyError: If no tool is registered with that name.
        """
        if tool_name not in self._tools:
            raise KeyError(f"Tool not found: {tool_name!r}")
        return self._tools[tool_name]
