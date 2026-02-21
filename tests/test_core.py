"""Tests for core validation functions."""

from __future__ import annotations

from pyturnstile._core import (
    _additional_validation,  # type: ignore
)
from pyturnstile._types import TurnstileResponse


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
