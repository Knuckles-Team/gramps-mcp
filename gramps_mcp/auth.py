#!/usr/bin/python

"""Runtime-only authentication for a configured Gramps Web API authority."""

from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from .api import Api

logger = get_logger(__name__)
_client: Api | None = None


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

    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        is_delegation_enabled,
    )

    delegated = is_delegation_enabled(config)
    explicit = any(
        value is not None for value in (url, token, username, password, tls_profile)
    )
    if not delegated and not explicit and _client is not None:
        return _client

    base_url = url or setting("GRAMPS_URL", "")
    if not base_url:
        raise RuntimeError("GRAMPS_URL is required")
    fixed_token = token or setting("GRAMPS_TOKEN", "")
    fixed_username = username or setting("GRAMPS_USERNAME", "")
    fixed_password = password or setting("GRAMPS_PASSWORD", "")
    if not delegated:
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

    profile = tls_profile or resolve_configured_tls_profile("gramps")

    if delegated:
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", base_url),
                scopes=(config or {}).get("delegated_scopes", "api"),
            )
            logger.info("Using OIDC delegated credentials")
            return Api(url=base_url, token=delegated_token, tls_profile=profile)
        except Exception as exc:
            profile.cleanup()
            logger.error(
                "OIDC delegation failed", extra={"error_type": type(exc).__name__}
            )
            raise RuntimeError("Token exchange failed") from None

    logger.info("Using fixed credentials")
    try:
        client = Api(
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

    if not explicit:
        _client = client
    return client
