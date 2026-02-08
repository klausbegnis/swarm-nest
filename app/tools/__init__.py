"""
File: __init__.py
Project: swarm-nest
Created: Sunday, 8th February 2026 6:02:43 pm
Author: Klaus Begnis

Copyright (c) 2026 Swarm Nest. See LICENSE for details.
"""

from .weather import INVOKE_PARAMS_EXAMPLE as weather_invoke_params
from .weather import get_weather

tools = [
    get_weather,
]

# Tool name -> example invoke params for tests (from each tool module).
TOOL_INVOKE_PARAMS_EXAMPLES: dict[str, dict] = {
    get_weather.name: weather_invoke_params,
}
