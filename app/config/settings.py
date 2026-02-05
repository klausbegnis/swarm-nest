"""
File: settings.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.
    Loads variables from .env automatically.
    Immutable and thread-safe.
    """

    # Application
    APP_NAME: str = "FastAPI Template"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # Server
    HOST: str = "localhost"
    PORT: int = 8000
    WORKERS: int = 1

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Database (loaded from .env; fallback for local dev)
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/swarm_nest"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        frozen=True,  # Makes settings immutable
        extra="ignore",  # Ignore extra variables in .env
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns singleton instance of Settings.
    Thread-safe due to lru_cache.
    Loads .env only once.

    Returns:
        Settings: Single configuration instance.
    """
    return Settings()


# Global instance for direct imports (startup, initial config)
settings = get_settings()

# Type alias for dependency injection (routers, services, tests)
SettingsDep = Annotated[Settings, Depends(get_settings)]
