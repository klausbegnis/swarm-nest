"""
File: test_agent_factory.py
Project: swarm-nest
Created: Sunday, 8th February 2026
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from unittest.mock import MagicMock, patch

from langchain.tools import BaseTool
from pydantic import BaseModel
import pytest

from app.factories.agent_factory import AgentConfig, AgentFactory
from app.schemas.db.agent import AgentCreate


@pytest.fixture
def factory() -> AgentFactory:
    """AgentFactory instance."""
    return AgentFactory()


@pytest.fixture
def minimal_agent_create() -> AgentCreate:
    """AgentCreate with required config (model, system_prompt)."""
    return AgentCreate(
        name="TestAgent",
        config={
            "model": "gpt-4",
            "system_prompt": "You are a helpful assistant.",
            "tools": ["get_weather"],
            "structured_output": None,
        },
    )


@pytest.mark.unit
def test_config_to_langchain_config_returns_agent_config(
    factory: AgentFactory, minimal_agent_create: AgentCreate
) -> None:
    """_config_to_langchain_config returns AgentConfig with resolved tools."""
    config = factory._config_to_langchain_config(minimal_agent_create)
    assert isinstance(config, AgentConfig)
    assert config.name == "TestAgent"
    assert config.model == "gpt-4"
    assert config.system_prompt == "You are a helpful assistant."
    assert isinstance(config.tools, list)
    assert len(config.tools) == 1
    assert isinstance(config.tools[0], BaseTool)
    assert config.tools[0].name == "get_weather"
    assert config.response_format is None


@pytest.mark.unit
def test_config_to_langchain_config_missing_model_raises(
    factory: AgentFactory,
) -> None:
    """Missing 'model' in config raises ValueError."""
    data = AgentCreate(
        name="X",
        config={
            "system_prompt": "Hi",
            "tools": None,
            "structured_output": None,
        },
    )
    with pytest.raises(ValueError, match="model"):
        factory._config_to_langchain_config(data)


@pytest.mark.unit
def test_config_to_langchain_config_missing_system_prompt_raises(
    factory: AgentFactory,
) -> None:
    """Missing 'system_prompt' in config raises ValueError."""
    data = AgentCreate(
        name="X",
        config={
            "model": "gpt-4",
            "tools": None,
            "structured_output": None,
        },
    )
    with pytest.raises(ValueError, match="system_prompt"):
        factory._config_to_langchain_config(data)


@pytest.mark.unit
def test_config_to_langchain_config_with_structured_output(
    factory: AgentFactory,
) -> None:
    """Config with structured_output builds response_format model class."""
    data = AgentCreate(
        name="X",
        config={
            "model": "gpt-4",
            "system_prompt": "Hi",
            "tools": None,
            "structured_output": [
                {"type": "int", "field_name": "count"},
                {"type": "str", "field_name": "label"},
            ],
        },
    )
    config = factory._config_to_langchain_config(data)
    assert config.response_format is not None
    assert isinstance(config.response_format, type)
    assert issubclass(config.response_format, BaseModel)
    # Can instantiate with schema
    obj = config.response_format(count=1, label="x")
    assert obj.count == 1
    assert obj.label == "x"


@pytest.mark.unit
def test_config_to_langchain_config_empty_tools(
    factory: AgentFactory,
) -> None:
    """Config with tools=None or missing yields empty tools list."""
    data = AgentCreate(
        name="X",
        config={
            "model": "gpt-4",
            "system_prompt": "Hi",
            "tools": None,
            "structured_output": None,
        },
    )
    config = factory._config_to_langchain_config(data)
    assert config.tools == []


@pytest.mark.unit
@patch("app.factories.agent_factory.create_agent")
def test_create_agent_calls_langchain_create_agent(
    mock_create_agent: MagicMock,
    factory: AgentFactory,
    minimal_agent_create: AgentCreate,
) -> None:
    """create_agent(AgentCreate) calls LangChain create_agent with config."""
    mock_create_agent.return_value = "mock_agent"
    result = factory.create_agent(minimal_agent_create)
    assert result == "mock_agent"
    mock_create_agent.assert_called_once()
    (_, call_kwargs) = mock_create_agent.call_args
    assert call_kwargs["name"] == "TestAgent"
    assert call_kwargs["model"] == "gpt-4"
    assert call_kwargs["system_prompt"] == "You are a helpful assistant."
    assert len(call_kwargs["tools"]) == 1
    assert call_kwargs["response_format"] is None
