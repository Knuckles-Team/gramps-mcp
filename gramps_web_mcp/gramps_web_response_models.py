#!/usr/bin/python
"""Pydantic response models for Gramps Web API payloads.

Gramps objects (people, families, events, …) are returned as JSON dicts and
wrapped by :class:`gramps_web_mcp.gramps_web_models.Response`. This lightweight
model is a convenience for the auth ``/api/token/`` exchange response.
"""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """The Gramps Web ``/api/token/`` login response."""

    access_token: str | None = Field(
        default=None, description="Short-lived JWT access token."
    )
    refresh_token: str | None = Field(
        default=None, description="Long-lived JWT refresh token."
    )
