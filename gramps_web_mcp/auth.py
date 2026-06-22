#!/usr/bin/python

"""Authentication for the Gramps Web API.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via the
   shared ``agent_utilities.mcp.delegated_auth`` helper.
2. **Fixed credentials** — a pre-minted JWT bearer token (``GRAMPS_WEB_TOKEN``) or a
   username/password login (``GRAMPS_WEB_USERNAME`` / ``GRAMPS_WEB_PASSWORD``)
   exchanged against ``/api/token/``.

Credentials resolve live through the shared config layer (the one XDG
``config.json`` / env), read at call time rather than frozen at import.
"""

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from gramps_web_mcp.api_client import Api

logger = get_logger(__name__)


def get_client(
    url: str | None = None,
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    verify: bool | None = None,
    config: dict | None = None,
) -> Api:
    """Factory function to create the Gramps Web :class:`Api` client.

    Resolves auth via OIDC delegation, a fixed bearer token, or username/password
    login. Settings read from the shared XDG config at call time.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    base_url = url if url is not None else setting("GRAMPS_WEB_URL")
    token = token if token is not None else setting("GRAMPS_WEB_TOKEN")
    username = username if username is not None else setting("GRAMPS_WEB_USERNAME")
    password = password if password is not None else setting("GRAMPS_WEB_PASSWORD")
    if verify is None:
        verify = setting("GRAMPS_WEB_SSL_VERIFY", True)

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if is_delegation_enabled(config):
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", base_url),
                scopes=(config or {}).get("delegated_scopes", "api"),
                verify=verify,
            )
            identity = get_user_identity()
            logger.info(
                "Using OIDC delegated token for Gramps Web API",
                extra={"user_email": identity.get("email"), "url": base_url},
            )
            return Api(url=base_url, token=delegated_token, verify=verify)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for Gramps Web",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}") from e

    # --- Path 2: Fixed Credentials (token or username/password login) ---
    logger.info("Using fixed credentials for Gramps Web API")
    try:
        return Api(
            url=base_url,
            token=token,
            username=username,
            password=password,
            verify=verify,
        )
    except (AuthError, UnauthorizedError) as e:
        raise RuntimeError(
            "AUTHENTICATION ERROR: The Gramps Web credentials provided are not "
            f"valid for '{base_url}'. Check GRAMPS_WEB_URL and GRAMPS_WEB_TOKEN "
            "(or GRAMPS_WEB_USERNAME / GRAMPS_WEB_PASSWORD). "
            f"Error details: {str(e)}"
        ) from e
