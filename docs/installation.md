# Installation

Python 3.11 through 3.14 is supported.

## Select a runtime

```bash
# MCP server
uvx --from "gramps-mcp[mcp]" gramps-mcp

# A2A agent
uvx --from "gramps-mcp[agent]" gramps-agent
```

For a durable environment:

```bash
uv pip install "gramps-mcp[mcp]"
uv pip install "gramps-mcp[agent]"
```

The `[mcp]` extra adds the MCP server surface. The `[agent]` extra adds the current
`agent-runtime` and Logfire. Agent Utilities itself always brings the supported
`epistemic-graph[full]` runtime; no numeric-only profile or second Python optimizer is
needed.

## Source checkout

```bash
git clone https://github.com/Knuckles-Team/gramps-mcp.git
uv sync --all-extras
```

Do not replace the package dependency with a local path or unpublished Git pin in a
release artifact. If the required Agent Utilities floor is not yet available from the
selected registry, publish that dependency first and regenerate the lockfile afterward.

## Containers

```bash
docker build --target mcp -t gramps-mcp:mcp -f docker/Dockerfile .
docker build --target agent -t gramps-mcp:agent-local -f docker/Dockerfile .
```

The runtime image receives endpoints, credentials, trust profiles, model configuration,
and observability settings only when it is launched.
