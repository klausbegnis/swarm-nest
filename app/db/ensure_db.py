"""
File: ensure_db.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def ensure_database_exists(database_url: str) -> None:
    """Create the application database if it does not exist.

    Connects to the default 'postgres' database and runs CREATE DATABASE
    for the database name in database_url when missing.

    Args:
        database_url (str): Full SQLAlchemy URL including the target database name.
    """
    url = make_url(database_url)
    db_name = url.database
    if not db_name or db_name == "postgres":
        return
    url_postgres = url.set(database="postgres")
    engine = create_engine(
        url_postgres,
        isolation_level="AUTOCOMMIT",
        pool_pre_ping=True,
    )
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
        )
        if result.scalar() is None:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
