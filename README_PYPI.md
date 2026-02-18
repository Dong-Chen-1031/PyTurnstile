<div align="center">
 <h1>PyTurnstile</h1>
 <a href="https://pypi.org/project/pyturnstile" target="_blank">
    <img src="https://github.com/Dong-Chen-1031/pyturnstile/blob/main/img/logo.png?raw=true" width="300" alt="Cloudflare Turnstile widget" />
 </a>
 <p>A Python library for validating <a href="https://developers.cloudflare.com/turnstile/">Cloudflare Turnstile</a> tokens with both async and sync support.</p>

<a href="https://github.com/dong-chen-1031/pyturnstile/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/dong-chen-1031/pyturnstile/actions/workflows/test.yml/badge.svg?event=push&branch=main" alt="Test">
</a>
<a href="https://pypi.org/project/pyturnstile" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyturnstile?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pyturnstile" target="_blank">
    <img src="https://img.shields.io/badge/Python-3.8%2B?color=%2334D058&logo=Python&logoColor=rgb(255%2C%20255%2C%20255)" alt="Supported Python versions">
</a>
<a href="https://docs.astral.sh/ruff/" target="_blank">
    <img src="https://camo.githubusercontent.com/d6c7524504b7d886a9d34c11f44b9d31b2de1a579325b42e932744c4575a063b/68747470733a2f2f696d672e736869656c64732e696f2f656e64706f696e743f75726c3d68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f61737472616c2d73682f727566662f6d61696e2f6173736574732f62616467652f76322e6a736f6e" alt="Ruff" />
</a>
<img src="https://img.shields.io/badge/License-MIT-%2334D058.svg" alt="License: MIT" />
<a href="https://github.com/dong-chen-1031/pyturnstile/pulls" target="_blank">
 <img src="https://img.shields.io/badge/PRs-welcome-%2334D058.svg" alt="PRs are welcome" />
</a>
</div>

## Features

- 🔄 Async & Sync Support
- 🚀 Simple API
- 📦 Lightweight - Only requires `httpx`

## What is PyTurnstile?

PyTurnstile simplifies Cloudflare Turnstile token validation. It handles all communication with Cloudflare's API.

<img src="https://github.com/Dong-Chen-1031/pyturnstile/blob/main/img/turnstile_verification.svg?raw=true" alt="Sequence diagram showing how PyTurnstile works" />

> Learn more at: https://developers.cloudflare.com/turnstile/

## Installation

Install the package using your preferred dependency manager.

### uv

```bash
uv add pyturnstile
```

### pip

```bash
pip install pyturnstile
```

## Usage

> ### 💡 TIP
>
> You can follow [this documentation](https://developers.cloudflare.com/turnstile/get-started/) and create your own Turnstile secret key at the [Cloudflare Turnstile dashboard](https://dash.cloudflare.com/?to=/:account/turnstile).

### Quick Start

PyTurnstile provides two ways to validate tokens:

#### 1. Using the `Turnstile` class (Recommended)

```python
from pyturnstile import Turnstile

turnstile = Turnstile(secret="your-secret-key")

response = await turnstile.async_validate(token="user-token-from-frontend")

# or validate synchronously
# response = turnstile.validate(token="user-token-from-frontend")

if response.success:
    print("✅ Token is valid!")
```

#### 2. Using functions directly

```python
from pyturnstile import validate, async_validate

response = await async_validate(
    token="user-token-from-frontend",
    secret="your-secret-key"
)

# or validate synchronously
# response = validate(
#     token="user-token-from-frontend",
#     secret="your-secret-key"
# )

if response.success:
    print("✅ Token is valid!")
```

### Optional Parameters

> ### ℹ️ NOTE
>
> For more details on all available parameters, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#required-parameters)

```python
response = turnstile.validate(
    token="user-token",               # The token from the client-side widget
    idempotency_key="unique-uuid",    # Optional: UUID for retry protection
    expected_remoteip="203.0.113.1",  # Optional: The visitor's IP address that the challenge response must match
    expected_hostname="example.com",  # Optional: The hostname that the challenge response must match
    expected_action="submit_form",    # Optional: The action identifier that the challenge must match
    timeout=10                        # Optional: request timeout in seconds
)
```

### Response Object

> ### ℹ️ NOTE
>
> For more details on all response fields, see the [Cloudflare documentation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/#response-fields)

The `TurnstileResponse` object contains:

```python
response.success                   # bool: Whether validation succeeded
response.error_codes               # list[TurnstileErrorCodes]: Error codes (if any)
response.challenge_ts              # str: ISO timestamp of challenge completion
response.hostname                  # str: Hostname where challenge was served
response.action                    # str: Custom action identifier
response.cdata                     # str: Custom data payload from client-side
response.metadata["ephemeral_id"]  # Device fingerprint ID (Enterprise only)
```

## Contributing

Any contributions are greatly appreciated. If you have a suggestion that would make this project better, please fork the repo and create a Pull Request. You can also [open an issue](https://github.com/Dong-Chen-1031/pyturnstile/issues).

## License

Published under the [MIT License](LICENSE).
