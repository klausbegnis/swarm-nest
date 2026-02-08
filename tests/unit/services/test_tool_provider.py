"""
File: test_tool_provider.py
Project: swarm-nest
Created: Sunday, 8th February 2026
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from langchain.tools import BaseTool
import pytest

from app.services.tool_provider import ToolProvider
from app.tools.weather import get_weather


@pytest.fixture
def provider() -> ToolProvider:
    """ToolProvider instance (uses app.tools list)."""
    return ToolProvider()


@pytest.mark.unit
def test_tools_property_returns_dict(provider: ToolProvider) -> None:
    """tools property returns a dict[str, BaseTool]."""
    tools = provider.tools
    assert isinstance(tools, dict)
    assert all(isinstance(v, BaseTool) for v in tools.values())
    assert all(isinstance(k, str) for k in tools)


@pytest.mark.unit
def test_get_tool_returns_tool(provider: ToolProvider) -> None:
    """get_tool(name) returns the registered BaseTool."""
    tool = provider.get_tool("get_weather")
    assert tool is get_weather
    assert tool.name == "get_weather"


@pytest.mark.unit
def test_get_tool_unknown_raises_key_error(provider: ToolProvider) -> None:
    """get_tool(unknown_name) raises KeyError."""
    with pytest.raises(KeyError, match="Tool not found"):
        provider.get_tool("nonexistent_tool")


@pytest.mark.unit
def test_tools_contains_registered_tools(provider: ToolProvider) -> None:
    """Provider contains all tools from app.tools (by name)."""
    assert "get_weather" in provider.tools
    assert provider.tools["get_weather"] is get_weather
