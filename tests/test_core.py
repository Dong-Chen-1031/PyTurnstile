"""Tests for core validation functions."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

import pytest

from pyturnstile._core import (
    _additional_validation,
    async_validate,
    validate,
)
from pyturnstile._types import TurnstileResponse, TurnstileValidationError


class TestAdditionalValidation:
    """Test _additional_validation function."""

    def test_successful_validation(self, mock_success_response):
        """Test validation with successful response and no additional checks."""
        result = _additional_validation(
            mock_success_response,
            expected_hostname=None,
            expected_action=None,
        )

        assert isinstance(result, TurnstileResponse)
        assert result.success is True

    def test_hostname_match(self, mock_success_response):
        """Test validation with matching hostname."""
        result = _additional_validation(
            mock_success_response,
            expected_hostname="example.com",
            expected_action=None,
        )

        assert result.success is True

    def test_hostname_mismatch(self, mock_success_response):
        """Test validation with mismatched hostname."""
        result = _additional_validation(
            mock_success_response,
            expected_hostname="different.com",
            expected_action=None,
        )

        assert result.success is False
        assert "hostname-mismatch" in result.error_codes

    def test_action_match(self, mock_success_response):
        """Test validation with matching action."""
        result = _additional_validation(
            mock_success_response,
            expected_hostname=None,
            expected_action="login",
        )

        assert result.success is True

    def test_action_mismatch(self, mock_success_response):
        """Test validation with mismatched action."""
        result = _additional_validation(
            mock_success_response,
            expected_hostname=None,
            expected_action="signup",
        )

        assert result.success is False
        assert "action-mismatch" in result.error_codes

    def test_failed_response_skips_additional_checks(self, mock_failure_response):
        """Test that additional checks are skipped for already failed response."""
        result = _additional_validation(
            mock_failure_response,
            expected_hostname="example.com",
            expected_action="login",
        )

        assert result.success is False
        assert "hostname-mismatch" not in result.error_codes
        assert "action-mismatch" not in result.error_codes


class TestValidate:
    """Test synchronous validate function."""

    @patch("pyturnstile._core.httpx.Client")
    def test_successful_validation(
        self, mock_client, mock_token, mock_secret, mock_success_response
    ):
        """Test successful token validation."""
        mock_response = Mock()
        mock_response.json.return_value = mock_success_response
        mock_response.raise_for_status = Mock()

        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_context)
        mock_context.__exit__ = Mock(return_value=False)
        mock_context.post = Mock(return_value=mock_response)
        mock_client.return_value = mock_context

        result = validate(token=mock_token, secret=mock_secret)

        assert isinstance(result, TurnstileResponse)
        assert result.success is True
        mock_context.post.assert_called_once()

    @patch("pyturnstile._core.httpx.Client")
    def test_validation_with_all_parameters(
        self, mock_client, mock_token, mock_secret, mock_success_response
    ):
        """Test validation with all optional parameters."""
        mock_response = Mock()
        mock_response.json.return_value = mock_success_response
        mock_response.raise_for_status = Mock()

        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_context)
        mock_context.__exit__ = Mock(return_value=False)
        mock_context.post = Mock(return_value=mock_response)
        mock_client.return_value = mock_context

        result = validate(
            token=mock_token,
            secret=mock_secret,
            idempotency_key="uuid-123",
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            timeout=20,
        )

        assert result.success is True
        call_args = mock_context.post.call_args
        assert call_args[1]["data"]["remoteip"] == "192.168.1.1"
        assert call_args[1]["data"]["idempotency_key"] == "uuid-123"

    @patch("pyturnstile._core.httpx.Client")
    def test_validation_network_error(self, mock_client, mock_token, mock_secret):
        """Test validation with network error."""
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_context)
        mock_context.__exit__ = Mock(return_value=False)
        mock_context.post = Mock(side_effect=Exception("Network error"))
        mock_client.return_value = mock_context

        with pytest.raises(TurnstileValidationError) as exc_info:
            validate(token=mock_token, secret=mock_secret)

        assert "Turnstile validation failed" in str(exc_info.value)


class TestAsyncValidate:
    """Test asynchronous validate function."""

    @pytest.mark.asyncio
    @patch("pyturnstile._core.httpx.AsyncClient")
    async def test_successful_validation(
        self, mock_client, mock_token, mock_secret, mock_success_response
    ):
        """Test successful async token validation."""
        mock_response = Mock()
        mock_response.json.return_value = mock_success_response
        mock_response.raise_for_status = Mock()

        mock_context = Mock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_context)
        mock_context.__aexit__ = AsyncMock(return_value=False)
        mock_context.post = AsyncMock(return_value=mock_response)
        mock_client.return_value = mock_context

        result = await async_validate(token=mock_token, secret=mock_secret)

        assert isinstance(result, TurnstileResponse)
        assert result.success is True
        mock_context.post.assert_called_once()

    @pytest.mark.asyncio
    @patch("pyturnstile._core.httpx.AsyncClient")
    async def test_validation_with_all_parameters(
        self, mock_client, mock_token, mock_secret, mock_success_response
    ):
        """Test async validation with all optional parameters."""
        mock_response = Mock()
        mock_response.json.return_value = mock_success_response
        mock_response.raise_for_status = Mock()

        mock_context = Mock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_context)
        mock_context.__aexit__ = AsyncMock(return_value=False)
        mock_context.post = AsyncMock(return_value=mock_response)
        mock_client.return_value = mock_context

        result = await async_validate(
            token=mock_token,
            secret=mock_secret,
            idempotency_key="uuid-123",
            expected_remoteip="192.168.1.1",
            expected_hostname="example.com",
            expected_action="login",
            timeout=20,
        )

        assert result.success is True
        call_args = mock_context.post.call_args
        assert call_args[1]["data"]["remoteip"] == "192.168.1.1"
        assert call_args[1]["data"]["idempotency_key"] == "uuid-123"

    @pytest.mark.asyncio
    @patch("pyturnstile._core.httpx.AsyncClient")
    async def test_validation_network_error(self, mock_client, mock_token, mock_secret):
        """Test async validation with network error."""
        mock_context = Mock()
        mock_context.__aenter__ = AsyncMock(return_value=mock_context)
        mock_context.__aexit__ = AsyncMock(return_value=False)
        mock_context.post = AsyncMock(side_effect=Exception("Network error"))
        mock_client.return_value = mock_context

        with pytest.raises(TurnstileValidationError) as exc_info:
            await async_validate(token=mock_token, secret=mock_secret)

        assert "Turnstile validation failed" in str(exc_info.value)
