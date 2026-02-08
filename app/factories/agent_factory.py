"""
File: agent_factory.py
Project: swarm-nest
Created: Sunday, 8th February 2026 5:51:32 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from dataclasses import asdict, dataclass
from typing import Any

from langchain.agents import create_agent
from langchain.tools import BaseTool
from pydantic import BaseModel

from app.factories.structured_output_factory import StructuredOutputFactory
from app.schemas.db.agent import AgentCreate
from app.services.tool_provider import ToolProvider


@dataclass
class AgentConfig:
    """
    Configuration for an agent.
    """

    name: str
    model: str
    system_prompt: str
    tools: list[BaseTool]
    response_format: type[BaseModel] | None = None


class AgentFactory:
    """
    Factory for creating agents.
    """

    def __init__(
        self,
        tool_provider: ToolProvider,
        structured_output_factory: StructuredOutputFactory,
    ) -> None:
        """
        Initialize the AgentFactory.
        """
        self.structured_output_factory = structured_output_factory
        self.tool_provider = tool_provider

    def create_agent(self, agent_config: AgentCreate) -> Any:
        """
        Create an agent from DB config.

        Args:
            agent_config: Configuration for the agent (from API/DB).

        Returns:
            The LangChain agent (runnable).
        """
        config = self._config_to_langchain_config(agent_config)
        agent = create_agent(**asdict(config))
        return agent

    def _config_to_langchain_config(
        self, agent_config: AgentCreate
    ) -> AgentConfig:
        """
        Convert an AgentCreate schema to an AgentConfig.

        Args:
            agent_config: AgentCreate schema.

        Returns:
            AgentConfig: Configuration for the agent.
        """
        cfg = agent_config.config
        model = cfg.get("model")
        system_prompt = cfg.get("system_prompt")
        if not model:
            raise ValueError("Agent config must have 'model'")
        if not system_prompt:
            raise ValueError("Agent config must have 'system_prompt'")

        structured_output = None
        if cfg.get("structured_output") is not None:
            structured_output = (
                self.structured_output_factory.create_structured_output_model(
                    fields=cfg["structured_output"],
                )
            )

        tools: list[BaseTool] = []
        if cfg.get("tools") is not None:
            for tool_name in cfg["tools"]:
                tools.append(self.tool_provider.get_tool(tool_name))
        return AgentConfig(
            name=agent_config.name,
            model=model,
            system_prompt=system_prompt,
            tools=tools,
            response_format=structured_output,
        )
