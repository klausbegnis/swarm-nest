"""
File: exceptions.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import get_logger

logger = get_logger(__name__)


class APIException(Exception):  # noqa: N818
    """
    Base exception class for custom API errors.

    Attributes:
        status_code: HTTP status code.
        detail: Error message detail.
        error_code: Machine-readable error code.
    """

    def __init__(
        self, status_code: int, detail: str, error_code: str | None = None
    ):
        """
        Initialize API exception.

        Args:
            status_code: HTTP status code.
            detail: Error message.
            error_code: Optional error code identifier.
        """
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code or "API_ERROR"
        super().__init__(self.detail)


class NotFoundException(APIException):
    """Exception for resource not found errors (404)."""

    def __init__(self, detail: str = "Resource not found"):
        """
        Initialize not found exception.

        Args:
            detail: Error message.
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND",
        )


class ValidationException(APIException):
    """Exception for validation errors (422)."""

    def __init__(self, detail: str):
        """
        Initialize validation exception.

        Args:
            detail: Error message.
        """
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR",
        )


class UnauthorizedException(APIException):
    """Exception for authentication errors (401)."""

    def __init__(self, detail: str = "Authentication required"):
        """
        Initialize unauthorized exception.

        Args:
            detail: Error message.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(APIException):
    """Exception for authorization errors (403)."""

    def __init__(self, detail: str = "Access forbidden"):
        """
        Initialize forbidden exception.

        Args:
            detail: Error message.
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN",
        )


# Exception Handlers


def api_exception_handler(request: Request, exc: APIException):
    """
    Handler for custom API exceptions.

    Args:
        request: FastAPI request object.
        exc: The raised API exception.

    Returns:
        JSONResponse: Standardized error response.
    """
    logger.warning(
        f"API Exception: {exc.error_code!s} - {exc.detail!s} - "
        f"Path: {request.url.path!s}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.detail,
            "path": str(request.url.path),
        },
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for Pydantic validation errors.

    Args:
        request: FastAPI request object.
        exc: The validation error.

    Returns:
        JSONResponse: Standardized validation error response.
    """
    logger.warning(
        f"Validation error on {request.url.path!s}: {exc.errors()!s}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid request data",
            "errors": exc.errors(),
            "path": str(request.url.path),
        },
    )


def general_exception_handler(request: Request, exc: Exception):
    """
    Handler for all unhandled exceptions.
    This is the last line of defense.

    Args:
        request: FastAPI request object.
        exc: The unhandled exception.

    Returns:
        JSONResponse: Standardized internal error response.
    """
    logger.error(f"Unhandled exception: {exc!s}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_ERROR",
            "message": "An internal error occurred",
            "path": str(request.url.path),
        },
    )
