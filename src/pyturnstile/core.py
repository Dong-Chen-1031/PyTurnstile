"""Async and sync functions to validate Turnstile tokens with Cloudflare's API."""

from __future__ import annotations

from typing import Any, Literal, Optional

import httpx


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
]
"""
Literal type for Turnstile error codes returned by the API.

For more details on all Turnstile error codes, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#error-codes-reference)
"""


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
    """Additional metadata returned by the API, including 'ephemeral_id' for device fingerprinting (Enterprise only)"""
    success: bool
    """Boolean indicating if validation was successful"""

    def __init__(self, data: dict) -> None:
        """
        Initialize the TurnstileResponse from the API response data.
        Args:
            data: The JSON response from the Turnstile API as a dictionary.
        """
        self.action = data.get("action", "")
        self.cdata = data.get("cdata", "")
        self.challenge_ts = data.get("challenge_ts", "")
        self.error_codes = data.get("error-codes", [])
        self.hostname = data.get("hostname", "")
        self.metadata = data.get("metadata", {})
        self.success = data.get("success", False)

    def __str__(self) -> str:
        return f"TurnstileResponse(success={self.success}, action={self.action}, hostname={self.hostname}, error_codes={self.error_codes})"

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return self.success

    def to_dict(self) -> dict:
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

    def model_dump(self) -> dict:
        """Alias for to_dict() to match common naming conventions."""
        return self.to_dict()


async def async_validate(
    token: str,
    secret: str,
    remoteip: Optional[str] = None,
    idempotency_key: Optional[str] = None,
    timeout: int = 10,
) -> TurnstileResponse:
    """
    Asynchronously validate a Turnstile token with Cloudflare's API.
    Args:
        secret: Your widget's secret key from the Cloudflare dashboard.
        token: The token from the client-side widget
        remoteip: (Optional) The visitor's IP address
        idempotency_key: (Optional) UUID for retry protection

    Returns:
        TurnstileResponse: The response from the Turnstile API

    For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
    """
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    data = {"secret": secret, "response": token}

    if remoteip:
        data["remoteip"] = remoteip

    if idempotency_key:
        data["idempotency_key"] = idempotency_key

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
            return TurnstileResponse(response.json())
    except Exception as e:
        raise TurnstileValidationError(f"Turnstile validation failed: {e}") from e


def validate(
    token: str,
    secret: str,
    remoteip: Optional[str] = None,
    idempotency_key: Optional[str] = None,
    timeout: int = 10,
) -> TurnstileResponse:
    """
    Validate a Turnstile token with Cloudflare's API.

    Args:
        secret: Your widget's secret key from the Cloudflare dashboard.
        token: The token from the client-side widget
        remoteip: (Optional) The visitor's IP address
        idempotency_key: (Optional) UUID for retry protection

    Returns:
        TurnstileResponse: The response from the Turnstile API

    For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
    """
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    data = {"secret": secret, "response": token}

    if remoteip:
        data["remoteip"] = remoteip

    if idempotency_key:
        data["idempotency_key"] = idempotency_key

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, data=data)
            response.raise_for_status()
            return TurnstileResponse(response.json())
    except Exception as e:
        raise TurnstileValidationError(f"Turnstile validation failed: {e}") from e


__all__ = [
    "TurnstileResponse",
    "TurnstileValidationError",
    "validate",
    "async_validate",
]
