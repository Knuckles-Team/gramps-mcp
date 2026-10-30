"""Public Gramps client package.

MCP and agent runtimes are explicit console entry points; importing the package never
starts or probes optional runtime surfaces.
"""

from gramps_mcp.api import Api, GrampsApiBase

__all__ = ["Api", "GrampsApiBase"]

from scion_sdk.connector import Connector

from gramps_mcp.api._operation_manifest import OPERATIONS
from gramps_mcp.auth import get_client

connector = Connector(
    tools="gramps_mcp.mcp",
    instructions="Gramps MCP Server — genealogy (people, families, events, places, sources, citations, media, notes, repositories, tags). Genealogy records are sensitive; use the governed condensed or verbose surface.",
    verbose_targets=(
        {"client_cls": Api, "get_client": get_client, "manifest": OPERATIONS},
    ),
)

__all__ = ["connector"]
