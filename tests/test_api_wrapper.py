from unittest.mock import patch

import pytest
import requests

from gramps_web_mcp.api_client import Api


def _make_response(status: int = 200, body: bytes = b"{}") -> requests.Response:
    resp = requests.Response()
    resp.status_code = status
    resp._content = body
    resp.headers["Content-Type"] = "application/json"
    return resp


@pytest.mark.concept("GRMP-001")
def test_call_returns_decoded_json():
    """A generated operation returns the decoded JSON body. CONCEPT:GRMP-001"""
    client = Api(url="https://gramps.arpa", token="t")
    resp = _make_response(200, b'{"people": []}')
    with patch.object(client, "_request", return_value=resp):
        result = client.get_people()
    assert result.data == {"people": []}
    assert result.status_code == 200


@pytest.mark.concept("GRMP-001")
def test_path_param_interpolated():
    """Path parameters are interpolated into the URL. CONCEPT:GRMP-001"""
    client = Api(url="https://gramps.arpa", token="t")
    captured = {}

    def fake_request(method, url, **kwargs):
        captured["url"] = url
        return _make_response(200, b"{}")

    with patch.object(client, "_request", side_effect=fake_request):
        client.get_person(handle="abc123")
    assert captured["url"].endswith("/api/people/abc123")
