#!/usr/bin/python

"""Runtime-only authentication for a configured Gramps Web API authority."""

from agent_connector_sdk.auth.delegation import DelegationSettings, delegated_token
from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile
from agent_connector_sdk.utilities import get_logger

from .api import Api

logger = get_logger(__name__)
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


def _build_delegated_client(
    base_url: str, settings: DelegationSettings, profile: ResolvedTLSProfile
) -> Api:
    try:
        token = delegated_token(settings)
        logger.info("Using OIDC delegated credentials")
        return Api(url=base_url, token=token, tls_profile=profile)
    except Exception as exc:
        profile.cleanup()
        logger.error(
            "OIDC delegation failed", extra={"error_type": type(exc).__name__}
        )
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
) -> Api:
    """Create a delegated or fixed-credential Gramps client.

    Endpoint, credentials, identity-provider configuration, and TLS trust resolve at
    runtime through AgentConfig. Delegated clients are request-scoped; the normal MCP
    dependency path reuses one fixed-credential client for the process lifetime.
    """
    global _client

    settings = DelegationSettings.from_settings()
    explicit = any(
        value is not None for value in (url, token, username, password, tls_profile)
    )
    if not settings.enabled and not explicit and _client is not None:
        return _client

    base_url, fixed_token, fixed_username, fixed_password = _resolve_client_credentials(
        url, token, username, password
    )
    if not settings.enabled:
        _validate_fixed_credential_mode(fixed_token, fixed_username, fixed_password)

    profile = tls_profile or resolve_tls_profile("gramps")

    if settings.enabled:
        return _build_delegated_client(base_url, settings, profile)

    client = _build_fixed_client(
        base_url, fixed_token, fixed_username, fixed_password, profile
    )
    if not explicit:
        _client = client
    return client
