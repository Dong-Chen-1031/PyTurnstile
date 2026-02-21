"""Tests for Turnstile client class."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from pyturnstile._turnstile import Turnstile
from pyturnstile._types import TurnstileResponse


class TestTurnstile:
    """Test Turnstile class."""

    def test_init(self, mock_secret):
        """Test Turnstile initialization."""
        turnstile = Turnstile(secret=mock_secret)
        assert turnstile.secret == mock_secret

    @patch("pyturnstile._turnstile._core.validate")
    def test_validate_method(self, mock_validate, mock_secret, mock_token):
        """Test synchronous validate method."""
        mock_response = Mock(spec=TurnstileResponse)
        mock_response.success = True
        mock_validate.return_value = mock_response

        turnstile = Turnstile(secret=mock_secret)
        result = turnstile.validate(token=mock_token)

        assert result.success is True
        mock_validate.assert_called_once_with(
            token=mock_token,
            secret=mock_secret,
            expected_remoteip=None,
            expected_hostname=None,
            expected_action=None,
            idempotency_key=None,
            timeout=10,
        )

    @patch("pyturnstile._turnstile._core.validate")
    def test_validate_with_all_parameters(self, mock_validate, mock_secret, mock_token):
        """Test synchronous validate with all optional parameters."""
        mock_response = Mock(spec=TurnstileResponse)
        mock_response.success = True
        mock_validate.return_value = mock_response

        turnstile = Turnstile(secret=mock_secret)
        result = turnstile.validate(
            token=mock_token,
            idempotency_key="uuid-123",
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            timeout=15,
        )

        assert result.success is True
        mock_validate.assert_called_once_with(
            token=mock_token,
            secret=mock_secret,
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            idempotency_key="uuid-123",
            timeout=15,
        )

    @pytest.mark.asyncio
    @patch("pyturnstile._turnstile._core.async_validate")
    async def test_async_validate_method(
        self, mock_async_validate, mock_secret, mock_token
    ):
        """Test asynchronous validate method."""
        mock_response = Mock(spec=TurnstileResponse)
        mock_response.success = True
        mock_async_validate.return_value = mock_response

        turnstile = Turnstile(secret=mock_secret)
        result = await turnstile.async_validate(token=mock_token)

        assert result.success is True
        mock_async_validate.assert_called_once_with(
            token=mock_token,
            secret=mock_secret,
            expected_remoteip=None,
            expected_hostname=None,
            expected_action=None,
            idempotency_key=None,
            timeout=10,
        )

    @pytest.mark.asyncio
    @patch("pyturnstile._turnstile._core.async_validate")
    async def test_async_validate_with_all_parameters(
        self, mock_async_validate, mock_secret, mock_token
    ):
        """Test asynchronous validate with all optional parameters."""
        mock_response = Mock(spec=TurnstileResponse)
        mock_response.success = True
        mock_async_validate.return_value = mock_response

        turnstile = Turnstile(secret=mock_secret)
        result = await turnstile.async_validate(
            token=mock_token,
            idempotency_key="uuid-123",
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            timeout=15,
        )

        assert result.success is True
        mock_async_validate.assert_called_once_with(
            token=mock_token,
            secret=mock_secret,
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            idempotency_key="uuid-123",
            timeout=15,
        )
