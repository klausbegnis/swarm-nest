"""
File: health.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
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
