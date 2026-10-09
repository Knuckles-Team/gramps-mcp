#!/usr/bin/python

"""Runtime-only authentication for a configured Gramps Web API authority."""

import logging
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile

from .api import Api

logger = logging.getLogger(__name__)
_client: Api | None = None


def _resolve_client_credentials(
    url: str | None,
    token: str | None,
    username: str | None,
    password: str | None,
) -> tuple[str, str, str, str]:
    base_url = url or setting("GRAMPS_URL", "")
    if not base_url:
        raise RuntimeError("GRAMPS_URL is required")
    fixed_token = token or setting("GRAMPS_TOKEN", "")
    fixed_username = username or setting("GRAMPS_USERNAME", "")
    fixed_password = password or setting("GRAMPS_PASSWORD", "")
    return base_url, fixed_token, fixed_username, fixed_password


def _validate_fixed_credential_mode(
    fixed_token: str, fixed_username: str, fixed_password: str
) -> None:
    if fixed_token and (fixed_username or fixed_password):
        raise RuntimeError(
            "Configure either GRAMPS_TOKEN or the username/password pair"
        )
    if bool(fixed_username) != bool(fixed_password):
        raise RuntimeError(
            "GRAMPS_USERNAME and GRAMPS_PASSWORD must be configured together"
        )
    if not fixed_token and not (fixed_username and fixed_password):
        raise RuntimeError(
            "GRAMPS_TOKEN or GRAMPS_USERNAME/GRAMPS_PASSWORD is required"
        )


def is_delegation_enabled(config: dict[str, Any] | None = None) -> bool:
    """Whether OIDC token delegation is active.

    An explicit ``config`` dict (test injection only) wins outright; otherwise
    reads the real ``ENABLE_DELEGATION`` setting through
    ``agent_connector_sdk.auth.delegation.DelegationSettings``.
    """
    if config is not None:
        return bool(config.get("enable_delegation", False))
    from agent_connector_sdk.auth.delegation import DelegationSettings

    return DelegationSettings.from_settings().enabled


def get_delegated_token(config: dict[str, Any] | None = None) -> str:
    """Exchange the verified caller token for a downstream Gramps token (RFC 8693).

    Reads delegation settings (``OIDC_TOKEN_URL``/``OIDC_CLIENT_ID``/
    ``OIDC_CLIENT_SECRET_REF``/``AUDIENCE``/``DELEGATED_SCOPES``) from the process
    settings via ``agent_connector_sdk.auth.delegation.DelegationSettings``; unlike the
    old ``agent_utilities`` helper, there is no per-call ``config`` override for those
    fields, only for whether delegation is attempted at all (see
    :func:`is_delegation_enabled`).
    """
    import httpx
    from agent_connector_sdk.auth.delegation import (
        DelegationSettings,
        current_user_token,
        exchange_token,
    )
    from agent_connector_sdk.exceptions import LoginRequiredError

    settings = DelegationSettings.from_settings()
    subject_token = current_user_token()
    if not subject_token:
        raise LoginRequiredError("no verified caller token to delegate")
    with httpx.Client(timeout=30) as http_client:
        access_token = exchange_token(
            settings, subject_token=subject_token, http_client=http_client
        )
    return access_token.value


def _build_delegated_client(
    base_url: str, config: dict[str, Any] | None, profile: ResolvedTLSProfile
) -> Api:
    try:
        delegated_token = get_delegated_token(config=config)
        logger.info("Using OIDC delegated credentials")
        return Api(url=base_url, token=delegated_token, tls_profile=profile)
    except Exception as exc:
        profile.cleanup()
        logger.error("OIDC delegation failed", extra={"error_type": type(exc).__name__})
        raise RuntimeError("Token exchange failed") from None


def _build_fixed_client(
    base_url: str,
    fixed_token: str,
    fixed_username: str,
    fixed_password: str,
    profile: ResolvedTLSProfile,
) -> Api:
    logger.info("Using fixed credentials")
    try:
        return Api(
            url=base_url,
            token=fixed_token or None,
            username=fixed_username or None,
            password=fixed_password or None,
            tls_profile=profile,
        )
    except (AuthError, UnauthorizedError):
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: The configured Gramps credentials were rejected"
        ) from None
    except Exception as exc:
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: Failed to instantiate the Gramps client "
            f"({type(exc).__name__})"
        ) from None


def get_client(
    url: str | None = None,
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict[str, Any] | None = None,
) -> Api:
    """Create a delegated or fixed-credential Gramps client.

    Endpoint, credentials, identity-provider configuration, and TLS trust resolve at
    runtime through AgentConfig. Delegated clients are request-scoped; the normal MCP
    dependency path reuses one fixed-credential client for the process lifetime.
    """
    global _client

    delegated = is_delegation_enabled(config)
    explicit = any(
        value is not None for value in (url, token, username, password, tls_profile)
    )
    if not delegated and not explicit and _client is not None:
        return _client

    base_url, fixed_token, fixed_username, fixed_password = _resolve_client_credentials(
        url, token, username, password
    )
    if not delegated:
        _validate_fixed_credential_mode(fixed_token, fixed_username, fixed_password)

    profile = tls_profile or resolve_tls_profile("gramps")

    if delegated:
        return _build_delegated_client(base_url, config, profile)

    client = _build_fixed_client(
        base_url, fixed_token, fixed_username, fixed_password, profile
    )
    if not explicit:
        _client = client
    return client
