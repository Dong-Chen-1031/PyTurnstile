"""Async and sync functions to validate Turnstile tokens with Cloudflare's API."""

from __future__ import annotations

from typing import Optional

import httpx

from ._types import (
    TurnstileResponse,
    TurnstileValidationError,
    _TurnstileResponseDictCF,  # type: ignore
)


def _additional_validation(
    response: _TurnstileResponseDictCF,
    expected_hostname: Optional[str],
    expected_action: Optional[str],
) -> TurnstileResponse:
    """
    Perform additional validation checks on the TurnstileResponse.

    Args:
        response: The raw response dictionary from the Turnstile API.
        expected_hostname: The expected hostname to match against the response.
        expected_action: The expected action identifier to match against the response.
    """

    if not response["success"]:
        return TurnstileResponse(response)

    if expected_hostname and response["hostname"] != expected_hostname:
        response["error-codes"] = ["hostname-mismatch"]
        response["success"] = False
        return TurnstileResponse(response)

    if expected_action and response["action"] != expected_action:
        response["error-codes"] = ["action-mismatch"]
        response["success"] = False
        return TurnstileResponse(response)

    return TurnstileResponse(response)


async def async_validate(
    token: str,
    secret: str,
    *,
    idempotency_key: Optional[str] = None,
    expected_remoteip: Optional[str] = None,
    expected_hostname: Optional[str] = None,
    expected_action: Optional[str] = None,
    timeout: int = 10,
) -> TurnstileResponse:
    """
    Asynchronously validate a Turnstile token with Cloudflare's API.
    Args:
        secret: Your widget's secret key from the Cloudflare dashboard.
        token: The token from the client-side widget
        idempotency_key: (Optional) UUID for retry protection
        expected_remoteip: (Optional) The visitor's IP address that the challenge response must match
        expected_hostname: (Optional) The hostname that the challenge response must match.
        expected_action: (Optional) The action identifier that the challenge must match.
        timeout: (Optional) Timeout for the API request in seconds
    Returns:
        TurnstileResponse: The response from the Turnstile API

    For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
    """
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    data = {"secret": secret, "response": token}

    if expected_remoteip:
        data["remoteip"] = expected_remoteip

    if idempotency_key:
        data["idempotency_key"] = idempotency_key

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, data=data)
            response.raise_for_status()
            return _additional_validation(
                response.json(), expected_hostname, expected_action
            )
    except Exception as e:
        raise TurnstileValidationError(f"Turnstile validation failed: {e}") from e


def validate(
    token: str,
    secret: str,
    *,
    idempotency_key: Optional[str] = None,
    expected_remoteip: Optional[str] = None,
    expected_hostname: Optional[str] = None,
    expected_action: Optional[str] = None,
    timeout: int = 10,
) -> TurnstileResponse:
    """
    Validate a Turnstile token with Cloudflare's API.

    Args:
        secret: Your widget's secret key from the Cloudflare dashboard.
        token: The token from the client-side widget
        idempotency_key: (Optional) UUID for retry protection
        expected_remoteip: (Optional) The visitor's IP address that the challenge response must match
        expected_hostname: (Optional) The hostname that the challenge response must match.
        expected_action: (Optional) The action identifier that the challenge must match.
        timeout: (Optional) Timeout for the API request in seconds
    Returns:
        TurnstileResponse: The response from the Turnstile API

    For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
    """
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

    data = {"secret": secret, "response": token}

    if expected_remoteip:
        data["remoteip"] = expected_remoteip

    if idempotency_key:
        data["idempotency_key"] = idempotency_key

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, data=data)
            response.raise_for_status()
            return _additional_validation(
                response.json(), expected_hostname, expected_action
            )
    except Exception as e:
        raise TurnstileValidationError(f"Turnstile validation failed: {e}") from e


__all__ = [
    "validate",
    "async_validate",
]
