#!/usr/bin/python
"""Pydantic input models for common Gramps Web API request parameters.

The generated domain clients accept arbitrary ``**kwargs`` (forwarded as path,
query, and body fields), so these models are convenience helpers for the most
common collection-query parameters rather than an exhaustive schema.
"""

from pydantic import BaseModel, Field


class CollectionQueryInput(BaseModel):
    """Common query parameters for Gramps Web collection endpoints."""

    gramps_id: str | None = Field(
        default=None, description="Filter by Gramps ID (e.g. 'I0001')."
    )
    page: int | None = Field(default=None, description="1-based page number.")
    pagesize: int | None = Field(default=None, description="Items per page.")
    keys: str | None = Field(
        default=None, description="Comma-separated object keys to include."
    )
    sort: str | None = Field(
        default=None, description="Comma-separated sort keys (prefix '-' to reverse)."
    )
