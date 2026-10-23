# CONN-GRAMPS-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `gramps-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `gramps_mcp` from it.
