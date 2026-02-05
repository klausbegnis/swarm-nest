"""
File: password.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Hash a plain password for storage.

    Args:
        plain (str): Plain-text password.

    Returns:
        str: Bcrypt-hashed password.
    """
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a hash.

    Args:
        plain (str): Plain-text password.
        hashed (str): Stored hash.

    Returns:
        bool: True if the password matches.
    """
    return pwd_context.verify(plain, hashed)
