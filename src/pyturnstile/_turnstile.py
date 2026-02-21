"""Client class for Cloudflare Turnstile token validation, providing both sync and async methods."""

from __future__ import annotations

from typing import Optional

from . import _core  # type: ignore


class Turnstile:
    """
    A client for validating Cloudflare Turnstile tokens.

    This class provides both synchronous and asynchronous methods to validate
    Turnstile tokens with Cloudflare's verification API.

    Methods:
        validate: Synchronously validate a Turnstile token.
        async_validate: Asynchronously validate a Turnstile token.

    Example:
        Asynchronous usage:
        >>> turnstile = Turnstile(secret="your-secret-key")
        >>> response = await turnstile.async_validate(token="user-token")
        >>> if response.success:
        ...     print("Valid token")

        Synchronous usage:
        >>> turnstile = Turnstile(secret="your-secret-key")
        >>> response = turnstile.validate(token="user-token")
        >>> if response.success:
        ...     print("Valid token")

    """

    def __init__(self, secret: str):
        """
        Initialize the Turnstile client with your secret key.
        Args:
            secret: Your widget's secret key from the Cloudflare dashboard.
        """
        self.secret = secret

    def validate(
        self,
        token: str,
        *,
        idempotency_key: Optional[str] = None,
        expected_remoteip: Optional[str] = None,
        expected_hostname: Optional[str] = None,
        expected_action: Optional[str] = None,
        timeout: int = 10,
    ) -> _core.TurnstileResponse:
        """
        Validate a Turnstile token with Cloudflare's API.
        Args:
            token: The token from the client-side widget
            idempotency_key: (Optional) UUID for retry protection
            expected_remoteip: (Optional) The visitor's IP address that the challenge response must match
            expected_hostname: (Optional) The hostname that the challenge response must match.
            expected_action: (Optional) The action identifier that the challenge must match.
            timeout: (Optional) Timeout for the API request in seconds
        Returns:
            TurnstileResponse: The response from the Turnstile API
        Raises:
            TurnstileValidationError: If the validation fails due to an API error or network issue

        For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
        """
        return _core.validate(
            token=token,
            secret=self.secret,
            expected_remoteip=expected_remoteip,
            expected_hostname=expected_hostname,
            expected_action=expected_action,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def async_validate(
        self,
        token: str,
        *,
        idempotency_key: Optional[str] = None,
        expected_remoteip: Optional[str] = None,
        expected_hostname: Optional[str] = None,
        expected_action: Optional[str] = None,
        timeout: int = 10,
    ) -> _core.TurnstileResponse:
        """
        Asynchronously validate a Turnstile token with Cloudflare's API.
        Args:
            token: The token from the client-side widget
            idempotency_key: (Optional) UUID for retry protection
            expected_remoteip: (Optional) The visitor's IP address that the challenge response must match
            expected_hostname: (Optional) The hostname that the challenge response must match.
            expected_action: (Optional) The action identifier that the challenge must match.
            timeout: (Optional) Timeout for the API request in seconds
        Returns:
            TurnstileResponse: The response from the Turnstile API
        Raises:
            TurnstileValidationError: If the validation fails due to an API error or network issue

        For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)
        """
        return await _core.async_validate(
            token=token,
            secret=self.secret,
            expected_remoteip=expected_remoteip,
            expected_hostname=expected_hostname,
            expected_action=expected_action,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


__all__ = ["Turnstile"]
