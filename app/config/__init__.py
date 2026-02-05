"""
File: __init__.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from .settings import SettingsDep, get_settings, settings

__all__ = ["settings", "get_settings", "SettingsDep"]
