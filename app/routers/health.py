"""
File: health.py
Project: replace with your project name
Created: Wednesday, 29th October 2025 4:13:25 pm
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
"""

from fastapi import APIRouter

from app.schemas.api import HealthResponse, SuccessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=SuccessResponse[HealthResponse])
def health() -> SuccessResponse[HealthResponse]:
    """
    Health check endpoint.

    Returns:
        SuccessResponse[HealthResponse]: Standardized health status response.
    """
    return SuccessResponse(
        message="Service is healthy", data=HealthResponse(status="ok")
    )
