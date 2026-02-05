"""
File: health.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health response model.
    """

    status: str
