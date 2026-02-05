"""
File: conftest.py
Project: replace with your project name
Created: Wednesday, 29th October 2025
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
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
