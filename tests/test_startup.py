import importlib

import pytest


@pytest.mark.concept("GM-OS.identity.grmp")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:GM-OS.identity.grmp"""
    assert importlib.import_module("gramps_mcp.mcp_server") is not None
