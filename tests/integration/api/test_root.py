"""
File: test_root.py
Project: swarm-nest
Created: Thursday, 05th February 2026
Author: Klaus Begnis

Copyright (c) 2025 Swarm Nest. See LICENSE for details.
"""

from fastapi.testclient import TestClient
import pytest


@pytest.mark.integration
def test_read_root(client: TestClient) -> None:
    """
    Test root endpoint.

    Args:
        client: TestClient fixture.
    """
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "app" in data
    assert "version" in data
    assert "message" in data
    assert data["message"] == "Hello, World!"


@pytest.mark.integration
def test_api_returns_json(client: TestClient) -> None:
    """
    Verify API returns JSON.

    Args:
        client: TestClient fixture.
    """
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"


@pytest.mark.integration
def test_success_response_format(client: TestClient) -> None:
    """
    Test standardized success response format.

    Args:
        client: TestClient fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "message" in data
    assert "data" in data
