"""
File: weather.py
Project: swarm-nest
Created: Sunday, 8th February 2026 6:01:55 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from langchain.tools import tool

# Example invoke params for tests (must match input schema).
INVOKE_PARAMS_EXAMPLE: dict = {"city": "London"}


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."
