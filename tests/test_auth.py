from unittest.mock import MagicMock, patch

import pytest

import gramps_mcp.auth as auth_module
from gramps_mcp.auth import get_client


@pytest.mark.concept("GM-OS.identity.grmp")
def test_get_client_auth_error_is_sanitized():
    """Client construction failure omits credential and provider details."""
    from agent_utilities.core.exceptions import AuthError

    auth_module._client = None
    profile = MagicMock()
    with patch(
        "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
        return_value=False,
    ):
        with patch("gramps_mcp.auth.Api", side_effect=AuthError("provider detail")):
            with pytest.raises(RuntimeError) as exc_info:
                get_client(
                    url="https://service.example.invalid",
                    token="runtime-token",
                    tls_profile=profile,
                )
    assert "AUTHENTICATION ERROR" in str(exc_info.value)
    assert "provider detail" not in str(exc_info.value)
    profile.cleanup.assert_called_once()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_get_client_builds_current_api_client():
    """A runtime token and resolved TLS profile build the composite client."""
    sentinel = object()
    profile = MagicMock()
    with patch(
        "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
        return_value=False,
    ):
        with patch("gramps_mcp.auth.Api", return_value=sentinel) as api_class:
            client = get_client(
                url="https://service.example.invalid",
                token="runtime-token",
                tls_profile=profile,
            )
    assert client is sentinel
    api_class.assert_called_once_with(
        url="https://service.example.invalid",
        token="runtime-token",
        username=None,
        password=None,
        tls_profile=profile,
    )


@pytest.mark.concept("GM-OS.identity.grmp")
def test_get_client_rejects_ambiguous_fixed_credentials():
    """A deployment cannot combine bearer and password authentication."""
    with patch(
        "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
        return_value=False,
    ):
        with pytest.raises(RuntimeError, match="either GRAMPS_TOKEN"):
            get_client(
                url="https://service.example.invalid",
                token="runtime-token",
                username="runtime-user",
                password="runtime-password",
            )
