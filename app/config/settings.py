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
    Configurações da aplicação.
    Carrega automaticamente variáveis do arquivo .env
    Imutável e thread-safe.
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        frozen=True,  # Torna as settings imutáveis
        extra="ignore",  # Ignora variáveis extras no .env
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância singleton de Settings.
    Thread-safe devido ao lru_cache.
    Carrega o .env apenas uma vez.

    Returns:
        Settings: Instância única de configurações.
    """
    return Settings()


# Instância global para imports diretos (startup, config inicial)
settings = get_settings()

# Type alias para dependency injection (routers, services, testes)
SettingsDep = Annotated[Settings, Depends(get_settings)]
