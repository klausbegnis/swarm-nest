"""
File: logger.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

import logging
import sys

from app.config import settings

# Códigos ANSI para cores (terminal)
_RESET = "\033[0m"
_DIM = "\033[2m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"
_BOLD_RED = "\033[1;31m"

LEVEL_COLORS = {
    logging.DEBUG: _DIM,
    logging.INFO: _GREEN,
    logging.WARNING: _YELLOW,
    logging.ERROR: _RED,
    logging.CRITICAL: _BOLD_RED,
}


class ColoredFormatter(logging.Formatter):
    """
    Formatter que adiciona cores por nível e formata como
    [horário] (arquivo): mensagem.
    """

    def __init__(self) -> None:
        """Inicializa com formato [horário] (arquivo): mensagem."""
        super().__init__(
            fmt="[%(asctime)s] (%(filename)s): %(message)s",
            datefmt="%H:%M:%S",
        )

    def format(self, record: logging.LogRecord) -> str:
        """Formata o registro e aplica cor quando a saída é um TTY."""
        color = LEVEL_COLORS.get(record.levelno, _RESET)
        formatted = super().format(record)
        if sys.stdout.isatty() and color != _RESET:
            return f"{color}{formatted}{_RESET}"
        return formatted


def setup_logging() -> None:
    """
    Configura o logging da aplicação.
    Nível e handler vêm das settings (env LOG_LEVEL).
    """
    log_level_str = getattr(settings, "LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    root = logging.getLogger()
    root.setLevel(log_level)

    # Remove handlers existentes para não duplicar
    for h in root.handlers[:]:
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(ColoredFormatter())
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger configurado com o formato [horário] (arquivo): mensagem.

    Args:
        name: Nome do logger (em geral __name__).

    Returns:
        Logger configurado.
    """
    return logging.getLogger(name)
