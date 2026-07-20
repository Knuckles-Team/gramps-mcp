from unittest.mock import MagicMock, patch

import pytest
import requests

from gramps_mcp.api import Api


def _profile() -> MagicMock:
    profile = MagicMock()
    profile.configure_requests_session.side_effect = lambda session: session
    return profile


def _make_response(status: int = 200, body: bytes = b"{}") -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response._content = body
    response.headers["Content-Type"] = "application/json"
    return response


@pytest.mark.concept("GM-OS.identity.grmp")
def test_call_returns_decoded_json():
    """A generated operation returns decoded JSON. CONCEPT:GM-OS.identity.grmp"""
    client = Api(
        url="https://service.example.invalid",
        token="test-token",
        tls_profile=_profile(),
    )
    response = _make_response(200, b'{"people": []}')
    with patch.object(client, "_request", return_value=response):
        result = client.get_people()
    assert result.data == {"people": []}
    assert result.status_code == 200


@pytest.mark.concept("GM-OS.identity.grmp")
def test_path_parameter_is_encoded_and_rebased():
    """Generated paths stay on the configured authority and encode path values."""
    client = Api(
        url="https://service.example.invalid",
        token="test-token",
        tls_profile=_profile(),
    )
    captured: dict[str, str] = {}

    def fake_request(method, url, **kwargs):
        captured["url"] = url
        return _make_response()

    with patch.object(client, "_request", side_effect=fake_request):
        client.get_person(handle="record/segment")
    assert (
        captured["url"] == "https://service.example.invalid/api/people/record%2Fsegment"
    )


@pytest.mark.concept("GM-OS.identity.grmp")
def test_client_rejects_cleartext_or_hidden_url_authority():
    """Endpoint configuration cannot weaken or hide the service authority."""
    with pytest.raises(Exception, match="absolute HTTPS URL"):
        Api(url="http://service.example.invalid", token="test-token")
    with pytest.raises(Exception, match="must not contain credentials"):
        Api(url="https://user@service.example.invalid", token="test-token")
    with pytest.raises(Exception, match="query or fragment"):
        Api(url="https://service.example.invalid?tree=one", token="test-token")


@pytest.mark.concept("GM-OS.identity.grmp")
def test_client_rejects_header_control_characters():
    """Bearer credentials cannot inject additional request headers."""
    with pytest.raises(Exception, match="GRAMPS_TOKEN is invalid"):
        Api(
            url="https://service.example.invalid",
            token="token\r\ninjected-header: value",
        )


@pytest.mark.concept("GM-OS.identity.grmp")
def test_requests_disable_redirects_and_reject_cross_authority():
    """Requests never follow redirects or escape the configured authority."""
    profile = _profile()
    client = Api(
        url="https://service.example.invalid", token="test-token", tls_profile=profile
    )
    with patch.object(
        client._session, "request", return_value=_make_response()
    ) as request:
        client._request("GET", "https://service.example.invalid/api/people/")
    assert request.call_args.kwargs["allow_redirects"] is False
    assert "verify" not in request.call_args.kwargs
    assert "proxies" not in request.call_args.kwargs
    with pytest.raises(Exception, match="authority differs"):
        client._request("GET", "https://other.example.invalid/api/people/")


@pytest.mark.concept("GM-OS.identity.grmp")
def test_auth_endpoint_error_does_not_expose_response_body():
    """Login failures expose a bounded class and status, never provider content."""
    client = Api(
        url="https://service.example.invalid",
        username="runtime-user",
        password="runtime-password",
        tls_profile=_profile(),
    )
    response = _make_response(500, b'{"detail":"sensitive-provider-message"}')
    with patch.object(client._session, "post", return_value=response):
        with pytest.raises(Exception) as exc_info:
            client._ensure_token()
    assert "sensitive-provider-message" not in str(exc_info.value)
