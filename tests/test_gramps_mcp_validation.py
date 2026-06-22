import pytest

from gramps_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("GRMP-001")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:GRMP-001
    """
    monkeypatch.setattr("sys.argv", ["gramps-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None
