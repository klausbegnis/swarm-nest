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
    Fixture that returns a TestClient to test the API.

    Returns:
        TestClient: FastAPI test client.
    """
    return TestClient(app)
