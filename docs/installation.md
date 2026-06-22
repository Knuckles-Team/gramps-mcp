# Installation

`gramps-web-mcp` is a standard Python package and a prebuilt container image.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable target service instance and access token.

## From PyPI (recommended)

```bash
pip install gramps-web-mcp
```

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "gramps-web-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "gramps-web-mcp[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "gramps-web-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/gramps-web-mcp.git
cd gramps-web-mcp
pip install -e ".[all]"
```

## Docker

```bash
docker pull knucklessg1/gramps-web-mcp:latest
```
