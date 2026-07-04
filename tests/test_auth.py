from unittest.mock import patch

import pytest

from gramps_mcp.auth import get_client


@pytest.mark.concept("GM-OS.identity.grmp")
def test_get_client_auth_error():
    """Auth failure surfaces a clear error. CONCEPT:GM-OS.identity.grmp"""
    from agent_utilities.core.exceptions import AuthError

    with patch(
        "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
        return_value=False,
    ):
        with patch("gramps_mcp.auth.Api", side_effect=AuthError("Auth Failure")):
            with pytest.raises(RuntimeError) as exc_info:
                get_client(url="https://gramps.arpa", token="bad")
    assert "AUTHENTICATION ERROR" in str(exc_info.value)


@pytest.mark.concept("GM-OS.identity.grmp")
def test_get_client_builds_api():
    """A valid token yields the composite Api client. CONCEPT:GM-OS.identity.grmp"""
    sentinel = object()
    with patch(
        "agent_utilities.mcp.delegated_auth.is_delegation_enabled",
        return_value=False,
    ):
        with patch("gramps_mcp.auth.Api", return_value=sentinel) as mock_cls:
            client = get_client(url="https://gramps.arpa", token="good")
    assert client is sentinel
    mock_cls.assert_called_once()
