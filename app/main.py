"""
File: main.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core import (
    APIException,
    api_exception_handler,
    general_exception_handler,
    get_logger,
    setup_logging,
    validation_exception_handler,
)
from .routers import health_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: RUF029
    """
    Application lifespan.

    Args:
        app (FastAPI): The FastAPI application.

    Yields:
        None: Application startup and shutdown context.
    """
    setup_logging()
    logger.info(f"Starting {settings.APP_NAME!s} v{settings.APP_VERSION!s}")
    logger.info(f"Debug mode: {settings.DEBUG!s}")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(health_router)


@app.get("/")
def read_root() -> dict:
    """
    Root endpoint.

    Returns:
        dict: Application info.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Hello, World!",
    }
