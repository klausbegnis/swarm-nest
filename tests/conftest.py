"""
File: conftest.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Fixture que retorna um TestClient para testar a API.

    Returns:
        TestClient: Cliente de teste do FastAPI.
    """
    return TestClient(app)
