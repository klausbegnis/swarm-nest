"""
File: health.py
Project: replace with your project name
Created: Wednesday, 29th October 2025 4:16:25 pm
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health response model.
    """

    status: str
