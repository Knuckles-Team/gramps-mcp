# Usage — API / CLI / MCP

`gramps-mcp` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** you import, and as a **CLI**.

## As an MCP server

Once [deployed](deployment.md), the server registers consolidated, action-routed
tool modules. Each module is independently togglable with a `*TOOL` environment
flag.

## As a Python API

```python
from gramps_mcp.auth import get_client

api = get_client()        # reads GRAMPS_WEB_URL / GRAMPS_WEB_TOKEN from the environment / .env
status = api.get_system_status()
```

## As a CLI

```bash
export GRAMPS_WEB_URL="http://localhost:8080"
export GRAMPS_WEB_TOKEN="your_token"
gramps-mcp --transport stdio
```
