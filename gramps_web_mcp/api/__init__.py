"""Gramps Web API client layer.

``api_client_base`` holds the hand-authored HTTP/auth/pagination machinery; the
``api_client_<domain>`` modules are generated from the vendored OpenAPI spec by
``scripts/generate_from_openapi.py`` and composed into the single ``Api`` class in
``gramps_web_mcp.api_client``.
"""

from .api_client_base import GrampsWebApiBase

__all__ = ["GrampsWebApiBase"]
