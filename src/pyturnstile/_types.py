"""Type definitions for PyTurnstile."""

from __future__ import annotations

from typing import Any, Literal, TypedDict, Union


class TurnstileValidationError(Exception):
    """Custom exception for Turnstile validation errors."""


TurnstileErrorCodes = Literal[
    "missing-input-secret",
    "invalid-input-secret",
    "missing-input-response",
    "invalid-input-response",
    "bad-request",
    "timeout-or-duplicate",
    "internal-error",
    "hostname-mismatch",
    "action-mismatch",
]
"""
Literal type for Turnstile error codes returned by the API.

For more details on all Turnstile error codes, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#error-codes-reference)
"""


_TurnstileResponseDictCF = TypedDict(
    "_TurnstileResponseDictCF",
    {
        "success": bool,
        "action": str,
        "cdata": str,
        "challenge_ts": str,
        "error-codes": Union[list[TurnstileErrorCodes], list[str]],
        "hostname": str,
        "metadata": dict[str, Any],
    },
)
"""Type definition for the TurnstileResponse form Cloudflare's API response."""

TurnstileResponseDict = TypedDict(
    "TurnstileResponseDict",
    {
        "success": bool,
        "action": str,
        "cdata": str,
        "challenge_ts": str,
        "error_codes": Union[list[TurnstileErrorCodes], list[str]],
        "hostname": str,
        "metadata": dict[str, Any],
    },
)
"""Type definition for the TurnstileResponse dictionary representation."""


class TurnstileResponse:
    """
    Represents the response from Cloudflare's Turnstile validation API.

    For more details on all response fields, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#response-fields)
    """

    action: str
    """Custom action identifier from client-side"""
    cdata: str
    """Custom data payload from client-side"""
    challenge_ts: str
    """ISO timestamp when the challenge was solved"""
    error_codes: list[TurnstileErrorCodes] | list[str]
    """Array of error codes (if validation failed)"""
    hostname: str
    """Hostname where the challenge was served"""
    metadata: dict[str, Any]
    """
    Additional metadata returned by the API.

    Including "ephemeral_id" for device fingerprinting (Enterprise only)
    """
    success: bool
    """Boolean indicating if validation was successful"""

    def __init__(self, data: TurnstileResponseDict | _TurnstileResponseDictCF) -> None:
        """
        Initialize the TurnstileResponse from the API response data.
        Args:
            data: The JSON response from the Turnstile API as a dictionary.
        """
        self.action = data.get("action", "")
        self.cdata = data.get("cdata", "")
        self.challenge_ts = data.get("challenge_ts", "")
        self.error_codes = data.get("error-codes", []) or data.get("error_codes", [])
        self.hostname = data.get("hostname", "")
        self.metadata = data.get("metadata", {})
        self.success = data.get("success", False)

    def to_dict(self) -> TurnstileResponseDict:
        """Convert the TurnstileResponse to a dictionary."""
        return {
            "success": self.success,
            "action": self.action,
            "cdata": self.cdata,
            "challenge_ts": self.challenge_ts,
            "error_codes": self.error_codes,
            "hostname": self.hostname,
            "metadata": self.metadata,
        }

    def model_dump(self) -> TurnstileResponseDict:
        """Alias for to_dict() to match common naming conventions."""
        return self.to_dict()

    def __str__(self) -> str:
        return (
            "TurnstileResponse("
            f"success={self.success}, "
            f"action={self.action}, "
            f"hostname={self.hostname}, "
            f"error_codes={self.error_codes}"
            ")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return self.success


__all__ = [
    "TurnstileResponse",
    "TurnstileValidationError",
    "TurnstileErrorCodes",
    "TurnstileResponseDict",
    "_TurnstileResponseDictCF",
]
