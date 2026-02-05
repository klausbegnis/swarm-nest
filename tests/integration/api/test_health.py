"""
File: test_health.py
Project: replace with your project name
Created: Wednesday, 29th October 2025
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
"""

from fastapi.testclient import TestClient
import pytest


@pytest.mark.integration
def test_health_endpoint(client: TestClient) -> None:
    """
    Test health check endpoint.

    Args:
        client: TestClient fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Service is healthy"
    assert data["data"]["status"] == "ok"


@pytest.mark.integration
def test_health_returns_json(client: TestClient) -> None:
    """
    Verify health check returns JSON.

    Args:
        client: TestClient fixture.
    """
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"
