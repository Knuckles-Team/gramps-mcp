import importlib

import pytest


@pytest.mark.concept("GRMP-001")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:GRMP-001"""
    assert importlib.import_module("gramps_mcp.mcp_server") is not None
