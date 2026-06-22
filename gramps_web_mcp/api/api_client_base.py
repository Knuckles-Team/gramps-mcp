#!/usr/bin/python
"""Base HTTP client for the Gramps Web API.

Handles the cross-cutting concerns shared by every generated domain client:

* **Authentication** — a pre-minted JWT bearer token (``GRAMPS_WEB_TOKEN``) or a
  username/password login (``GRAMPS_WEB_USERNAME`` / ``GRAMPS_WEB_PASSWORD``)
  exchanged against ``/api/token/`` for an access token, refreshed before expiry.
* **Single tenant host** — Gramps Web serves one tree-server instance per host
  (``GRAMPS_WEB_URL``, e.g. ``https://gramps.arpa``). Generated methods carry the
  absolute URL template from the spec; this base resolves ``{param}`` path tokens.
* **Pagination** — Gramps' offset style (``page`` / ``pagesize`` query params with a
  ``X-Total-Count`` header on collection responses).
* **Transient errors** — retries ``429`` / ``502`` / ``503`` / ``504`` with bounded
  exponential backoff, honouring ``Retry-After``.
"""

import logging
import threading
import time
from typing import Any, TypeVar

import requests
import urllib3
from agent_utilities.base_utilities import get_logger
from agent_utilities.core.exceptions import (
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)
from pydantic import ValidationError

from gramps_web_mcp.gramps_web_models import Response

logger = get_logger(__name__)

T = TypeVar("T")


class GrampsWebApiBase:
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        proxies: dict | None = None,
        verify: bool = True,
        max_retries: int = 3,
        debug: bool = False,
    ):
        logger.setLevel(logging.DEBUG if debug else logging.ERROR)

        self.verify = verify
        self.proxies = proxies
        self.debug = debug
        self.max_retries = max_retries
        self._session = requests.Session()
        self._token_lock = threading.Lock()
        self._token = token
        self._refresh_token: str | None = None
        self._token_expiry = 0.0
        self._username = username
        self._password = password

        host = (url or "").strip().rstrip("/")
        if not host:
            raise MissingParameterError(
                "Provide GRAMPS_WEB_URL (e.g. https://gramps.arpa)."
            )
        if not host.startswith(("http://", "https://")):
            host = f"https://{host}"
        self.url = host

        if self.verify is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if not self._token and not (self._username and self._password):
            raise MissingParameterError(
                "Provide GRAMPS_WEB_TOKEN, or GRAMPS_WEB_USERNAME and "
                "GRAMPS_WEB_PASSWORD for the login flow."
            )

    # ------------------------------------------------------------------ auth
    def _ensure_token(self) -> str:
        """Return a valid bearer token, logging in via username/password if needed."""
        if self._token and (
            not self._username or time.monotonic() < self._token_expiry
        ):
            return self._token
        with self._token_lock:
            if self._token and time.monotonic() < self._token_expiry:
                return self._token
            token_url = f"{self.url}/api/token/"
            try:
                resp = self._session.post(
                    url=token_url,
                    json={"username": self._username, "password": self._password},
                    headers={"Accept": "application/json"},
                    verify=self.verify,
                    proxies=self.proxies,
                    timeout=30,
                )
            except requests.RequestException as e:
                raise AuthError(f"Gramps Web token request failed: {e}") from e
            if resp.status_code in (401, 403):
                raise UnauthorizedError(
                    f"Gramps Web credentials rejected ({resp.status_code})."
                )
            if not resp.ok:
                raise AuthError(
                    f"Gramps Web token endpoint returned {resp.status_code}: "
                    f"{resp.text}"
                )
            payload = resp.json()
            self._token = payload.get("access_token") or payload.get("token")
            self._refresh_token = payload.get("refresh_token")
            if not self._token:
                raise AuthError("Gramps Web token response contained no access_token.")
            # Gramps access tokens default to 15 minutes; refresh 60s early.
            self._token_expiry = time.monotonic() + (15 * 60) - 60
            return self._token

    def _auth_headers(self, content_type: str | None = "application/json") -> dict:
        headers = {
            "Authorization": f"Bearer {self._ensure_token()}",
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    # --------------------------------------------------------------- url build
    def _resolve_url(self, url_template: str, path_kwargs: dict) -> str:
        """Resolve a spec URL template into an absolute URL.

        Interpolates ``{param}`` path parameters by name. A relative template is
        joined against ``self.url``.
        """
        url = url_template
        if "://" in url:
            # The spec baked an absolute server URL into the template; rebase its
            # path onto the configured base URL (scheme/host/port may differ — e.g.
            # the spec says https://gramps.arpa but the deployment serves http).
            from urllib.parse import urlsplit

            url = f"{self.url.rstrip('/')}{urlsplit(url).path}"
        elif url.startswith("/"):
            url = f"{self.url}{url}"
        for key, value in (path_kwargs or {}).items():
            url = url.replace("{" + key + "}", str(value))
        if "{" in url:
            missing = url[url.index("{") + 1 : url.index("}")] if "}" in url else "?"
            raise MissingParameterError(f"Missing required path parameter: {missing}")
        return url

    # ----------------------------------------------------------------- request
    def _request(
        self,
        method: str,
        url: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        """Perform an HTTP request with rate-limit / transient-error retries."""
        request_headers = headers or self._auth_headers()
        attempt = 0
        while True:
            response = self._session.request(
                method=method.upper(),
                url=url,
                params=params or None,
                json=json,
                data=data,
                headers=request_headers,
                verify=self.verify,
                proxies=self.proxies,
                timeout=60,
            )
            if response.status_code == 429 and attempt < self.max_retries:
                delay = self._retry_delay(response, attempt)
                logger.debug("Rate limited (429); sleeping %.1fs", delay)
                time.sleep(delay)
                attempt += 1
                continue
            if response.status_code in (502, 503, 504) and attempt < self.max_retries:
                time.sleep(self._retry_delay(response, attempt))
                attempt += 1
                continue
            if response.status_code in (401, 403):
                raise (AuthError if response.status_code == 401 else UnauthorizedError)(
                    f"Gramps Web request to {url} failed ({response.status_code})."
                )
            return response

    @staticmethod
    def _retry_delay(response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        if not response.content:
            return None
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except ValueError:
                return response.text
        return response.text

    # -------------------------------------------------------------- pagination
    def _fetch_all_pages(
        self, method: str, url: str, params: dict, max_pages: int
    ) -> tuple[requests.Response, list]:
        """Collect every page of a Gramps offset-paginated collection."""
        params = dict(params or {})
        first = self._request(method, url, params=params)
        body = self._decode(first)
        all_data = list(body) if isinstance(body, list) else self._extract_items(body)
        max_pages = max_pages if max_pages and max_pages > 0 else 10

        total = self._total_count(first)
        pagesize = int(params.get("pagesize", len(all_data) or 1) or 1)
        page = int(params.get("page", 1) or 1)
        fetched = len(all_data)
        while total and fetched < total and page < max_pages:
            page += 1
            params["page"] = page
            resp = self._request(method, url, params=params)
            chunk = self._decode(resp)
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
            val = response.headers.get(key)
            if val:
                try:
                    return int(val)
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
        """Dispatch a single generated operation. Used by every domain method."""
        try:
            kwargs = {k: v for k, v in (kwargs or {}).items() if v is not None}
            path_kwargs = {k: kwargs.pop(k) for k in path_params if k in kwargs}
            url = self._resolve_url(url_template, path_kwargs)

            params = {k: kwargs.pop(k) for k in query_params if k in kwargs}
            body = None
            if has_body:
                body = kwargs.pop("body", None)
                if body is None and kwargs:
                    body = kwargs
                    kwargs = {}
            # Remaining kwargs (unknown to the spec) fold into query params.
            params.update(kwargs)

            if http.upper() == "GET" and paginate == "offset":
                max_pages = int(params.pop("max_pages", 0) or 0)
                response, data = self._fetch_all_pages(http, url, params, max_pages)
                return Response(response=response, data=data)

            params.pop("max_pages", None)
            response = self._request(http, url, params=params, json=body)
            return Response(response=response, data=self._decode(response))
        except (AuthError, UnauthorizedError, MissingParameterError):
            raise
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            logger.error("Gramps Web request error: %s", e)
            raise

    # --------------------------------------------------------------- escape hatch
    def api_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> Response:
        """Make an arbitrary Gramps Web REST request against the configured host.

        ``endpoint`` is a path (e.g. ``/api/people/``) appended to the configured
        base URL. Use this for operations not covered by a typed method.
        """
        if method.upper() not in ("GET", "POST", "PUT", "DELETE", "PATCH"):
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        url = f"{self.url}/{endpoint.lstrip('/')}"
        response = self._request(method, url, params=params, json=json, data=data)
        return Response(response=response, data=self._decode(response))
