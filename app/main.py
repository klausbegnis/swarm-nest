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
from .db import Base, engine
from .db.ensure_db import ensure_database_exists
from .factories.agent_factory import AgentFactory
from .factories.structured_output_factory import StructuredOutputFactory
from .routers import (
    agent_router,
    health_router,
    prompt_router,
    role_router,
    user_router,
)
from .services.tool_provider import ToolProvider

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
    ensure_database_exists(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    logger.info("Starting factories...")
    structured_output_factory = StructuredOutputFactory()
    tool_provider = ToolProvider()
    agent_factory = AgentFactory(tool_provider, structured_output_factory)
    app.state.agent_factory = agent_factory
    logger.info("Agent Factory started - loading models from database...")
    # TODO: Load models from database
    logger.info("Database tables created or already exist")
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
app.include_router(agent_router)
app.include_router(prompt_router)
app.include_router(role_router)
app.include_router(user_router)


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
