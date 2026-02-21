"""Pytest configuration and shared fixtures."""

from typing import Any

import pytest


@pytest.fixture
def mock_secret():
    """Mock secret key for testing."""
    return "1x0000000000000000000000000000000AA"


@pytest.fixture
def mock_token():
    """Mock Turnstile token for testing."""
    return "test-token-12345"


@pytest.fixture
def mock_success_response() -> dict[str, Any]:
    """Mock successful API response."""
    return {
        "success": True,
        "challenge_ts": "2024-01-01T00:00:00.000Z",
        "hostname": "example.com",
        "error-codes": [],
        "action": "login",
        "cdata": "session123",
        "metadata": {"ephemeral_id": "device-123"},
    }


@pytest.fixture
def mock_failure_response() -> dict[str, Any]:
    """Mock failed API response."""
    return {
        "success": False,
        "error-codes": ["invalid-input-response"],
        "challenge_ts": "",
        "hostname": "",
        "action": "",
        "cdata": "",
    }
