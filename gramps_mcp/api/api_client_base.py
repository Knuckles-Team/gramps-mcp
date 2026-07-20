#!/usr/bin/python
"""Shared HTTPS, authentication, pagination, and response handling for Gramps."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, TypeVar
from urllib.parse import quote, urlsplit

import requests
from agent_utilities.base_utilities import get_logger
from agent_utilities.core.exceptions import (
    ApiError,
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)
from pydantic import ValidationError

from gramps_mcp.gramps_models import Response

logger = get_logger(__name__)

T = TypeVar("T")

_MAX_URL_BYTES = 2_048
_MAX_SECRET_BYTES = 65_536
_MAX_USERNAME_BYTES = 1_024
_MAX_PATH_VALUE_BYTES = 8_192
_MAX_RESPONSE_BYTES = 64 * 1024 * 1024
_TRANSIENT_STATUSES = {429, 502, 503, 504}


def _has_controls(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _invalid_url_text(value: str) -> bool:
    return (
        _has_controls(value)
        or "\\" in value
        or any(character.isspace() for character in value)
    )


def _validated_secret(
    value: str | None,
    *,
    label: str,
    maximum: int,
    header_value: bool = False,
) -> str:
    rendered = str(value or "")
    if (
        not 1 <= len(rendered.encode("utf-8")) <= maximum
        or _has_controls(rendered)
        or (header_value and any(character.isspace() for character in rendered))
    ):
        raise ParameterError(f"{label} is invalid")
    return rendered


class GrampsApiBase:
    """Base client used by every generated Gramps API domain mixin."""

    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
        max_retries: int = 3,
        debug: bool = False,
    ) -> None:
        logger.setLevel(logging.DEBUG if debug else logging.ERROR)
        if not isinstance(max_retries, int) or not 0 <= max_retries <= 10:
            raise ParameterError("max_retries must be between 0 and 10")

        host = str(url or "").strip().rstrip("/")
        if not 1 <= len(host.encode("utf-8")) <= _MAX_URL_BYTES or _invalid_url_text(
            host
        ):
            raise MissingParameterError("GRAMPS_URL is required and must be valid")
        parsed = urlsplit(host)
        try:
            _ = parsed.port
        except ValueError:
            raise ParameterError("GRAMPS_URL is invalid") from None
        if parsed.scheme != "https" or not parsed.hostname:
            raise ParameterError("GRAMPS_URL must be an absolute HTTPS URL")
        if parsed.username or parsed.password:
            raise ParameterError("GRAMPS_URL must not contain credentials")
        if parsed.query or parsed.fragment:
            raise ParameterError("GRAMPS_URL must not contain a query or fragment")

        if token and (username or password):
            raise ParameterError("Configure either a token or a username/password pair")
        if bool(username) != bool(password):
            raise MissingParameterError(
                "GRAMPS_USERNAME and GRAMPS_PASSWORD must be configured together"
            )
        if not token and not (username and password):
            raise MissingParameterError(
                "Configure GRAMPS_TOKEN or GRAMPS_USERNAME and GRAMPS_PASSWORD"
            )

        self.url = host
        self.debug = debug
        self.max_retries = max_retries
        self.tls_profile = tls_profile or resolve_configured_tls_profile("gramps")
        self._session = self.tls_profile.configure_requests_session(requests.Session())
        self._token_lock = threading.Lock()
        self._token = (
            _validated_secret(
                token,
                label="GRAMPS_TOKEN",
                maximum=_MAX_SECRET_BYTES,
                header_value=True,
            )
            if token
            else None
        )
        self._token_is_fixed = self._token is not None
        self._refresh_token: str | None = None
        self._token_expiry = float("inf") if self._token_is_fixed else 0.0
        self._username = (
            _validated_secret(
                username, label="GRAMPS_USERNAME", maximum=_MAX_USERNAME_BYTES
            )
            if username
            else None
        )
        self._password = (
            _validated_secret(
                password, label="GRAMPS_PASSWORD", maximum=_MAX_SECRET_BYTES
            )
            if password
            else None
        )

    def close(self) -> None:
        """Release the session, temporary TLS material, and in-memory credentials."""
        self._session.close()
        self._token = None
        self._refresh_token = None
        self._username = None
        self._password = None
        self.tls_profile.cleanup()

    # ------------------------------------------------------------------ auth
    def _token_request(self, path: str, payload: dict[str, str]) -> dict[str, Any]:
        try:
            response = self._session.post(
                url=f"{self.url}{path}",
                json=payload,
                headers={"Accept": "application/json"},
                timeout=30.0,
                allow_redirects=False,
            )
        except requests.RequestException:
            raise AuthError("Gramps token request failed") from None
        if response.status_code == 401:
            raise AuthError("Gramps credentials were rejected")
        if response.status_code == 403:
            raise UnauthorizedError("Gramps credentials are not authorized")
        if not 200 <= response.status_code < 300:
            raise AuthError(
                f"Gramps token endpoint returned HTTP {response.status_code}"
            )
        try:
            decoded = response.json()
        except ValueError:
            raise AuthError("Gramps token endpoint returned invalid JSON") from None
        if not isinstance(decoded, dict):
            raise AuthError("Gramps token endpoint returned an invalid response")
        return decoded

    def _accept_token_payload(self, payload: dict[str, Any]) -> str:
        access = (
            payload.get("access_token") or payload.get("access") or payload.get("token")
        )
        self._token = _validated_secret(
            access,
            label="Gramps access token",
            maximum=_MAX_SECRET_BYTES,
            header_value=True,
        )
        refresh = payload.get("refresh_token") or payload.get("refresh")
        self._refresh_token = (
            _validated_secret(
                refresh,
                label="Gramps refresh token",
                maximum=_MAX_SECRET_BYTES,
                header_value=True,
            )
            if refresh
            else None
        )
        expires_in = payload.get("expires_in", 15 * 60)
        try:
            lifetime = max(60.0, min(float(expires_in), 24 * 60 * 60))
        except (TypeError, ValueError):
            lifetime = 15 * 60
        self._token_expiry = time.monotonic() + max(1.0, lifetime - 60.0)
        return self._token

    def _ensure_token(self) -> str:
        """Return a fixed or current short-lived bearer token."""
        if self._token and (
            self._token_is_fixed or time.monotonic() < self._token_expiry
        ):
            return self._token
        with self._token_lock:
            if self._token and (
                self._token_is_fixed or time.monotonic() < self._token_expiry
            ):
                return self._token
            if self._refresh_token:
                try:
                    return self._accept_token_payload(
                        self._token_request(
                            "/api/token/refresh/",
                            {"refresh_token": self._refresh_token},
                        )
                    )
                except AuthError:
                    if not (self._username and self._password):
                        raise
            if not (self._username and self._password):
                raise AuthError("Gramps authentication must be renewed")
            return self._accept_token_payload(
                self._token_request(
                    "/api/token/",
                    {"username": self._username, "password": self._password},
                )
            )

    def _auth_headers(self, content_type: str | None = "application/json") -> dict:
        headers = {
            "Authorization": f"Bearer {self._ensure_token()}",
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    # --------------------------------------------------------------- url build
    def _resolve_url(self, url_template: str, path_kwargs: dict[str, Any]) -> str:
        """Resolve a generated relative template against the configured authority."""
        template = str(url_template or "")
        if not 1 <= len(
            template.encode("utf-8")
        ) <= _MAX_URL_BYTES or _invalid_url_text(template):
            raise ParameterError("API URL template is invalid")
        parsed = urlsplit(template)
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
            raise ParameterError("API URL template must be a relative path")
        path = template
        if not path.startswith("/"):
            path = "/" + path
        for key, value in (path_kwargs or {}).items():
            rendered = str(value)
            if not 1 <= len(
                rendered.encode("utf-8")
            ) <= _MAX_PATH_VALUE_BYTES or _has_controls(rendered):
                raise ParameterError("Path parameter is invalid")
            path = path.replace("{" + key + "}", quote(rendered, safe=""))
        if "{" in path or "}" in path:
            raise MissingParameterError("A required path parameter is missing")
        return f"{self.url}{path}"

    # ----------------------------------------------------------------- request
    def _request(
        self,
        method: str,
        url: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> requests.Response:
        """Perform one bounded request with transient retries and no redirects."""
        request_url = urlsplit(url)
        configured = urlsplit(self.url)
        if (
            request_url.scheme != configured.scheme
            or request_url.netloc != configured.netloc
        ):
            raise ParameterError("Request authority differs from GRAMPS_URL")

        attempt = 0
        while True:
            try:
                response = self._session.request(
                    method=method.upper(),
                    url=url,
                    params=params or None,
                    json=json,
                    data=data,
                    headers=self._auth_headers(),
                    timeout=60.0,
                    allow_redirects=False,
                )
            except requests.RequestException:
                raise ApiError("Gramps API request failed") from None
            if (
                response.status_code in _TRANSIENT_STATUSES
                and attempt < self.max_retries
            ):
                time.sleep(self._retry_delay(response, attempt))
                attempt += 1
                continue
            if response.status_code == 401:
                raise AuthError("Gramps API rejected the active credential")
            if response.status_code == 403:
                raise UnauthorizedError("Gramps API denied the requested operation")
            if not 200 <= response.status_code < 300:
                raise ApiError(f"Gramps API returned HTTP {response.status_code}")
            return response

    @staticmethod
    def _retry_delay(response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(max(float(retry_after), 0.0), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        content = response.content
        if not content:
            return None
        if len(content) > _MAX_RESPONSE_BYTES:
            raise ApiError("Gramps API response exceeded the connector limit")
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except ValueError:
                raise ApiError("Gramps API returned invalid JSON") from None
        return content

    # -------------------------------------------------------------- pagination
    def _fetch_all_pages(
        self, method: str, url: str, params: dict, max_pages: int
    ) -> tuple[requests.Response, list]:
        """Collect a bounded number of offset-paginated collection pages."""
        params = dict(params or {})
        first = self._request(method, url, params=params)
        body = self._decode(first)
        all_data = list(body) if isinstance(body, list) else self._extract_items(body)
        max_pages = max_pages if max_pages and max_pages > 0 else 10
        max_pages = min(max_pages, 1_000)

        total = self._total_count(first)
        pagesize = int(params.get("pagesize", len(all_data) or 1) or 1)
        page = int(params.get("page", 1) or 1)
        fetched = len(all_data)
        while total and fetched < total and page < max_pages:
            page += 1
            params["page"] = page
            response = self._request(method, url, params=params)
            chunk = self._decode(response)
            items = chunk if isinstance(chunk, list) else self._extract_items(chunk)
            if not items:
                break
            all_data.extend(items)
            fetched += len(items)
            if len(items) < pagesize:
                break
        return first, all_data

    @staticmethod
    def _extract_items(body: Any) -> list:
        if isinstance(body, list):
            return body
        if isinstance(body, dict):
            for key in ("data", "items", "results", "objects"):
                if isinstance(body.get(key), list):
                    return body[key]
        return []

    @staticmethod
    def _total_count(response: requests.Response) -> int:
        for key in ("X-Total-Count", "Total-Count"):
            value = response.headers.get(key)
            if value:
                try:
                    return max(int(value), 0)
                except ValueError:
                    pass
        return 0

    # ----------------------------------------------------------- generated call
    def _call(
        self,
        http: str,
        url_template: str,
        path_params: list[str],
        query_params: list[str],
        has_body: bool,
        paginate: str,
        kwargs: dict,
    ) -> Response:
        """Dispatch one generated operation."""
        try:
            kwargs = {
                key: value for key, value in (kwargs or {}).items() if value is not None
            }
            path_kwargs = {key: kwargs.pop(key) for key in path_params if key in kwargs}
            url = self._resolve_url(url_template, path_kwargs)

            params = {key: kwargs.pop(key) for key in query_params if key in kwargs}
            body = None
            if has_body:
                body = kwargs.pop("body", None)
                if body is None and kwargs:
                    body = kwargs
                    kwargs = {}
            params.update(kwargs)

            if http.upper() == "GET" and paginate == "offset":
                max_pages = int(params.pop("max_pages", 0) or 0)
                response, decoded = self._fetch_all_pages(http, url, params, max_pages)
                return Response(response=response, data=decoded)

            params.pop("max_pages", None)
            response = self._request(http, url, params=params, json=body)
            return Response(response=response, data=self._decode(response))
        except (
            ApiError,
            AuthError,
            UnauthorizedError,
            MissingParameterError,
            ParameterError,
        ):
            raise
        except ValidationError:
            raise ParameterError("Invalid API parameters") from None
        except (TypeError, ValueError):
            raise ParameterError("Invalid API parameters") from None

    def api_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> Response:
        """Call an unmodeled path on the configured authority without URL escape."""
        if method.upper() not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            raise ParameterError("Unsupported HTTP method")
        rendered = str(endpoint or "")
        parsed = urlsplit(rendered)
        if (
            not 1 <= len(rendered.encode("utf-8")) <= _MAX_URL_BYTES
            or _invalid_url_text(rendered)
            or parsed.scheme
            or parsed.netloc
            or parsed.query
            or parsed.fragment
            or any(segment == ".." for segment in parsed.path.split("/"))
        ):
            raise ParameterError("API endpoint path is invalid")
        url = self._resolve_url(parsed.path, {})
        response = self._request(method, url, params=params, json=json, data=data)
        return Response(response=response, data=self._decode(response))
