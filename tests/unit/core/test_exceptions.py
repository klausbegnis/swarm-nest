"""
File: test_exceptions.py
Project: replace with your project name
Created: Wednesday, 29th October 2025
Author: replace with your name

Copyright (c) 2025 replace with your company. All rights reserved.
"""

import pytest

from app.core import NotFoundException, ValidationException


@pytest.mark.unit
def test_not_found_exception() -> None:
    """
    Test NotFoundException properties.
    """
    exc = NotFoundException("Test resource not found")
    assert exc.status_code == 404
    assert exc.error_code == "NOT_FOUND"
    assert exc.detail == "Test resource not found"


@pytest.mark.unit
def test_not_found_exception_default_message() -> None:
    """
    Test NotFoundException with default message.
    """
    exc = NotFoundException()
    assert exc.status_code == 404
    assert exc.error_code == "NOT_FOUND"
    assert exc.detail == "Resource not found"


@pytest.mark.unit
def test_validation_exception() -> None:
    """
    Test ValidationException properties.
    """
    exc = ValidationException("Test validation failed")
    assert exc.status_code == 422
    assert exc.error_code == "VALIDATION_ERROR"
    assert exc.detail == "Test validation failed"
