"""Client identity reaches every prepared HTTP request without changing transport."""

import json
from importlib.metadata import version
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest
import requests

from gramps_mcp.api import Api
from gramps_mcp.api import api_client_base


@pytest.fixture
def transport(monkeypatch):
    replies: list[tuple[int, object, dict[str, str]]] = []
    sent = []

    def send(session, request, **kwargs):
        sent.append((request, kwargs))
        status, body, headers = replies.pop(0)
        response = requests.Response()
        response.status_code = status
        response._content = json.dumps(body).encode()
        response.headers.update({"Content-Type": "application/json", **headers})
        response.request = request
        return response

    def configure(session):
        session.trust_env = False
        session.verify = "/synthetic/ca.pem"
        session.cert = ("/synthetic/client.pem", "/synthetic/client.key")
        session.headers["X-TLS-Profile"] = "fixture"
        return session

    profile = MagicMock()
    profile.configure_requests_session.side_effect = configure
    monkeypatch.setattr(requests.Session, "send", send)
    monkeypatch.setattr(api_client_base.time, "sleep", lambda _delay: None)
    return profile, replies, sent


def _assert_transport(sent, authorizations, timeouts):
    assert len(sent) == len(authorizations) == len(timeouts)
    for (request, options), authorization, timeout in zip(
        sent, authorizations, timeouts, strict=True
    ):
        assert isinstance(request, requests.PreparedRequest)
        assert request.headers["User-Agent"] == f"gramps-mcp/{version('gramps-mcp')}"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
        assert request.headers.get("Authorization") == authorization
        assert request.headers["X-TLS-Profile"] == "fixture"
        assert options["verify"] == "/synthetic/ca.pem"
        assert options["cert"] == ("/synthetic/client.pem", "/synthetic/client.key")
        assert options["timeout"] == timeout
        assert options["allow_redirects"] is False
        assert options["proxies"] == {}


@pytest.mark.parametrize("method", ["GET", "POST"])
def test_fixed_token_api_requests_identify_installed_package(transport, method):
    profile, replies, sent = transport
    replies.append((200, {"ok": True}, {}))
    client = Api(
        url="https://service.example.invalid", token="fixed", tls_profile=profile
    )
    result = client.api_request(method, "/api/people/", json={"fixture": True})
    assert result.data == {"ok": True}
    assert json.loads(sent[0][0].body) == {"fixture": True}
    _assert_transport(sent, ["Bearer fixed"], [60.0])


def test_login_and_refresh_inherit_session_identity(transport):
    profile, replies, sent = transport
    replies.extend(
        [
            (200, {"access_token": "access-one", "refresh_token": "refresh-one"}, {}),
            (200, [], {}),
            (200, {"access_token": "access-two", "refresh_token": "refresh-two"}, {}),
            (200, [], {}),
        ]
    )
    client = Api(
        url="https://service.example.invalid",
        username="fixture-user",
        password="fixture-password",
        tls_profile=profile,
    )
    client.api_request("GET", "/api/people/")
    client._token_expiry = 0
    client.api_request("GET", "/api/people/")
    assert [urlsplit(request.url).path for request, _ in sent] == [
        "/api/token/",
        "/api/people/",
        "/api/token/refresh/",
        "/api/people/",
    ]
    assert json.loads(sent[0][0].body) == {
        "username": "fixture-user",
        "password": "fixture-password",
    }
    assert json.loads(sent[2][0].body) == {"refresh_token": "refresh-one"}
    _assert_transport(
        sent,
        [None, "Bearer access-one", None, "Bearer access-two"],
        [30.0, 60.0, 30.0, 60.0],
    )


def test_transient_retry_keeps_session_identity(transport):
    profile, replies, sent = transport
    replies.extend([(503, {}, {}), (200, {"ok": True}, {})])
    client = Api(
        url="https://service.example.invalid", token="fixed", tls_profile=profile
    )
    assert client.api_request("GET", "/api/people/").data == {"ok": True}
    assert sent[0][0].url == sent[1][0].url
    _assert_transport(sent, ["Bearer fixed"] * 2, [60.0] * 2)


def test_pagination_keeps_session_identity(transport):
    profile, replies, sent = transport
    replies.extend(
        [
            (200, [{"handle": "one"}], {"X-Total-Count": "2"}),
            (200, [{"handle": "two"}], {}),
        ]
    )
    client = Api(
        url="https://service.example.invalid", token="fixed", tls_profile=profile
    )
    _, data = client._fetch_all_pages(
        "GET",
        "https://service.example.invalid/api/people/",
        {"pagesize": 1, "page": 1},
        10,
    )
    assert data == [{"handle": "one"}, {"handle": "two"}]
    assert [parse_qs(urlsplit(request.url).query)["page"] for request, _ in sent] == [
        ["1"],
        ["2"],
    ]
    _assert_transport(sent, ["Bearer fixed"] * 2, [60.0] * 2)


def test_session_identity_uses_distribution_metadata(transport, monkeypatch):
    profile, _, _ = transport
    metadata_version = MagicMock(return_value="9.8.7rc1")
    monkeypatch.setattr(api_client_base, "version", metadata_version)
    client = Api(
        url="https://service.example.invalid", token="fixed", tls_profile=profile
    )
    assert client._session.headers["User-Agent"] == "gramps-mcp/9.8.7rc1"
    metadata_version.assert_called_once_with("gramps-mcp")
