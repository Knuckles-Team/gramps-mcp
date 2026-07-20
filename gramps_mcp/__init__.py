"""Public Gramps client package.

MCP and agent runtimes are explicit console entry points; importing the package never
starts or probes optional runtime surfaces.
"""

from gramps_mcp.api import Api, GrampsApiBase

__all__ = ["Api", "GrampsApiBase"]
