"""Public Gramps client package.

MCP and agent runtimes are explicit console entry points; importing the package never
starts or probes optional runtime surfaces.
"""

from gramps_mcp.api import Api, GrampsApiBase

__all__ = ["Api", "GrampsApiBase"]

from scion_sdk.connector import Connector

from gramps_mcp.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    instructions="Gramps MCP Server — genealogy (people, families, events, places, sources, citations, media, notes, repositories, tags). Genealogy records are sensitive; use the governed typed surface.",
)

__all__ = ["connector"]
