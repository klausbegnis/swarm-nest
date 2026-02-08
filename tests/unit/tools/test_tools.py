"""
File: test_tools.py
Project: swarm-nest
Created: Sunday, 8th February 2026
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.

Uses LangChain ToolsUnitTests for all tools from app.tools (one class per tool).
https://reference.langchain.com/python/langchain_tests/unit_tests/tools/#tool-unit-tests
"""

import sys

from langchain_tests.unit_tests.tools import ToolsUnitTests
import pytest

from app.tools import TOOL_INVOKE_PARAMS_EXAMPLES, tools as tools_list


def _class_name_for_tool(name: str) -> str:
    """e.g. get_weather -> TestGetWeatherStandard."""
    parts = name.split("_")
    pascal = "".join(p.capitalize() for p in parts)
    return f"Test{pascal}Standard"


# Create one ToolsUnitTests subclass per tool so LangChain's full suite runs.
for _tool in tools_list:
    if _tool.name not in TOOL_INVOKE_PARAMS_EXAMPLES:
        raise ValueError(
            f"Add INVOKE_PARAMS_EXAMPLE in the tool module for {_tool.name!r} "
            "and wire it in app.tools.__init__.py (TOOL_INVOKE_PARAMS_EXAMPLES)"
        )
    _tool_instance = _tool
    _invoke_params = TOOL_INVOKE_PARAMS_EXAMPLES[_tool.name]
    _name = _class_name_for_tool(_tool.name)
    _cls = type(
        _name,
        (ToolsUnitTests,),
        {
            "tool_constructor": property(lambda self, t=_tool_instance: t),
            "tool_constructor_params": property(lambda self: {}),
            "tool_invoke_params_example": property(
                lambda self, p=_invoke_params: p
            ),
        },
    )
    _cls = pytest.mark.unit(_cls)
    setattr(sys.modules[__name__], _name, _cls)
