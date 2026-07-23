#!/usr/bin/python

import logging
import sys
from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import load_config
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface

from gramps_mcp.api import Api
from gramps_mcp.api._operation_manifest import OPERATIONS
from gramps_mcp.auth import get_client
from gramps_mcp.mcp import TOOL_REGISTRY

__version__ = "2.0.0"

logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def get_mcp_instance() -> tuple[Any, Any, Any]:
    """Initialize and return the Gramps MCP instance, args, and middlewares.

    The whole tool surface is wired by the shared ``register_tool_surface`` helper
    per ``MCP_TOOL_MODE`` (read from the XDG config): ``condensed`` (action-routed
    tools), ``verbose`` (one named 1:1 tool per API method, fully typed from the
    OpenAPI manifest), or ``both`` (default). To add a domain, drop a
    ``register_<domain>_tools(mcp)`` into the ``mcp/`` package and re-export it from
    ``mcp/__init__.py`` (the generator does this) — it is auto-discovered and gated by
    ``setting("<DOMAIN>TOOL", True)``; no edit here is needed.
    """
    load_config()

    args, mcp, middlewares = create_mcp_server(
        name="Gramps MCP",
        version=__version__,
        instructions=(
            "Gramps MCP Server — genealogy (people, families, events, places, "
            "sources, citations, media, notes, repositories, tags). Genealogy "
            "records are sensitive; use the governed condensed or verbose surface."
        ),
    )

    register_tool_surface(
        mcp,
        service="gramps-mcp",
        client_cls=Api,
        get_client=get_client,
        tool_registry=TOOL_REGISTRY,
        manifest=OPERATIONS,
    )

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares


def mcp_server():
    mcp, args, _ = get_mcp_instance()

    print(f"Gramps MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
