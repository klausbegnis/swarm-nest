"""
File: base.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):  # noqa: UP046
    """
    Standardized success response model.

    Attributes:
        success: Always True for successful responses.
        message: Human-readable success message.
        data: Response payload (generic type).
    """

    success: bool = True
    message: str = "Success"
    data: T | None = None


class ErrorResponse(BaseModel):
    """
    Standardized error response model.

    Attributes:
        success: Always False for error responses.
        error_code: Machine-readable error code.
        message: Human-readable error message.
        errors: Optional list of detailed errors.
        path: API path where error occurred.
    """

    success: bool = False
    error_code: str
    message: str
    errors: list | None = None
    path: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):  # noqa: UP046
    """
    Standardized paginated response model.

    Attributes:
        success: Always True for successful responses.
        data: List of items (generic type).
        total: Total number of items.
        page: Current page number.
        page_size: Number of items per page.
        total_pages: Total number of pages.
    """

    success: bool = True
    data: list[T]
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
