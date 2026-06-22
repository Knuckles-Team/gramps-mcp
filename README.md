# Gramps Web MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/gramps-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/gramps-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gramps-mcp)
![PyPI - License](https://img.shields.io/pypi/l/gramps-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gramps-mcp)

*Version: 0.1.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing platform are maintained in the
> [official documentation](https://knuckles-team.github.io/gramps-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Available MCP Tools](#available-mcp-tools)
- [Installation](#installation)
- [Usage](#usage)
- [MCP](#mcp)
- [Documentation](#documentation)

---

## Overview

**Gramps Web MCP MCP Server + A2A Agent**

Gramps Web API + MCP Server + A2A Agent — genealogy (people/families/events/places/sources/media)

This repository is actively maintained - Contributions are welcome!

## Key Features

- **Action-routed MCP tools** — each domain is exposed as a single MCP tool that routes
  to many underlying operations via an `action` argument, keeping the tool surface small.
- **Three interfaces, one package** — use it as a Python **API client**, an **MCP server**
  (`stdio` / `streamable-http` / `sse`), or a Pydantic-AI **A2A agent**.
- **`agent-utilities` native** — built on the shared framework (auth, action router,
  telemetry, governance) for fleet consistency.
- **Per-tool toggles** — enable or disable each tool domain with environment switches.
- **Enterprise-ready** — OTEL/Langfuse telemetry and optional Eunomia access governance.

## Available MCP Tools

Each tool is **action-routed**: pass an `action` and a JSON `params_json` payload. Tool
domains can be toggled on or off with the listed environment variable. The table below is
**auto-generated from the live server** by the `mcp-readme-table` pre-commit hook
(`python -m agent_utilities.mcp.readme_tools`) — do not edit it by hand.

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `gramps_bookmarks` | `BOOKMARKSTOOL` | Manage Gramps Web bookmarks operations. CONCEPT:GRMP-001. |
| `gramps_chat` | `CHATTOOL` | Manage Gramps Web chat operations. CONCEPT:GRMP-001. |
| `gramps_citations` | `CITATIONSTOOL` | Manage Gramps Web citations operations. CONCEPT:GRMP-001. |
| `gramps_config` | `CONFIGTOOL` | Manage Gramps Web config operations. CONCEPT:GRMP-001. |
| `gramps_dna` | `DNATOOL` | Manage Gramps Web dna operations. CONCEPT:GRMP-001. |
| `gramps_events` | `EVENTSTOOL` | Manage Gramps Web events operations. CONCEPT:GRMP-001. |
| `gramps_exporters` | `EXPORTERSTOOL` | Manage Gramps Web exporters operations. CONCEPT:GRMP-001. |
| `gramps_facts` | `FACTSTOOL` | Manage Gramps Web facts operations. CONCEPT:GRMP-001. |
| `gramps_families` | `FAMILIESTOOL` | Manage Gramps Web families operations. CONCEPT:GRMP-001. |
| `gramps_filters` | `FILTERSTOOL` | Manage Gramps Web filters operations. CONCEPT:GRMP-001. |
| `gramps_holidays` | `HOLIDAYSTOOL` | Manage Gramps Web holidays operations. CONCEPT:GRMP-001. |
| `gramps_importers` | `IMPORTERSTOOL` | Manage Gramps Web importers operations. CONCEPT:GRMP-001. |
| `gramps_living` | `LIVINGTOOL` | Manage Gramps Web living operations. CONCEPT:GRMP-001. |
| `gramps_media` | `MEDIATOOL` | Manage Gramps Web media operations. CONCEPT:GRMP-001. |
| `gramps_metadata` | `METADATATOOL` | Manage Gramps Web metadata operations. CONCEPT:GRMP-001. |
| `gramps_name_formats` | `NAME_FORMATSTOOL` | Manage Gramps Web name formats operations. CONCEPT:GRMP-001. |
| `gramps_name_groups` | `NAME_GROUPSTOOL` | Manage Gramps Web name groups operations. CONCEPT:GRMP-001. |
| `gramps_notes` | `NOTESTOOL` | Manage Gramps Web notes operations. CONCEPT:GRMP-001. |
| `gramps_oidc` | `OIDCTOOL` | Manage Gramps Web oidc operations. CONCEPT:GRMP-001. |
| `gramps_people` | `PEOPLETOOL` | Manage Gramps Web people operations. CONCEPT:GRMP-001. |
| `gramps_places` | `PLACESTOOL` | Manage Gramps Web places operations. CONCEPT:GRMP-001. |
| `gramps_relations` | `RELATIONSTOOL` | Manage Gramps Web relations operations. CONCEPT:GRMP-001. |
| `gramps_reports` | `REPORTSTOOL` | Manage Gramps Web reports operations. CONCEPT:GRMP-001. |
| `gramps_repositories` | `REPOSITORIESTOOL` | Manage Gramps Web repositories operations. CONCEPT:GRMP-001. |
| `gramps_search` | `SEARCHTOOL` | Manage Gramps Web search operations. CONCEPT:GRMP-001. |
| `gramps_sources` | `SOURCESTOOL` | Manage Gramps Web sources operations. CONCEPT:GRMP-001. |
| `gramps_tags` | `TAGSTOOL` | Manage Gramps Web tags operations. CONCEPT:GRMP-001. |
| `gramps_tasks` | `TASKSTOOL` | Manage Gramps Web tasks operations. CONCEPT:GRMP-001. |
| `gramps_timeline` | `TIMELINETOOL` | Manage Gramps Web timeline operations. CONCEPT:GRMP-001. |
| `gramps_token` | `TOKENTOOL` | Manage Gramps Web token operations. CONCEPT:GRMP-001. |
| `gramps_transactions` | `TRANSACTIONSTOOL` | Manage Gramps Web transactions operations. CONCEPT:GRMP-001. |
| `gramps_translations` | `TRANSLATIONSTOOL` | Manage Gramps Web translations operations. CONCEPT:GRMP-001. |
| `gramps_trees` | `TREESTOOL` | Manage Gramps Web trees operations. CONCEPT:GRMP-001. |
| `gramps_types` | `TYPESTOOL` | Manage Gramps Web types operations. CONCEPT:GRMP-001. |
| `gramps_users` | `USERSTOOL` | Manage Gramps Web users operations. CONCEPT:GRMP-001. |

_35 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

### Install with `uvx` (no install — run on demand)

```bash
uvx --from gramps-mcp gramps-mcp      # MCP server
uvx --from gramps-mcp gramps-agent    # A2A agent server
```

### Install with `pip`

```bash
python -m pip install gramps-mcp            # core (API client)
python -m pip install "gramps-mcp[all]"     # + MCP server + A2A agent + telemetry
```

### Console scripts

After installation the following entry points are available on your `PATH`:

| Command | Description |
|---------|-------------|
| `gramps-mcp` | Launch the MCP server |
| `gramps-agent` | Launch the A2A agent server |

## Usage

### As a Python API client

```python
from gramps_mcp.auth import get_client

client = get_client()
status = client.get_system_status()
print(status)
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
gramps-mcp

# Networked streamable-http
gramps-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "system_operations",
  "arguments": {
    "action": "status",
    "params_json": "{}"
  }
}
```

## MCP

### Using as an MCP Server

The MCP Server can be run in `stdio` (local), `streamable-http` (networked), or
`sse` mode.

#### Environment Variables

*   `GRAMPS_WEB_URL`: The URL of the target service.
*   `GRAMPS_WEB_TOKEN`: The API token or access token.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "gramps-mcp": {
      "command": "uvx",
      "args": ["--from", "gramps-mcp", "gramps-mcp"],
      "env": {
        "GRAMPS_WEB_URL": "https://service.example.com",
        "GRAMPS_WEB_TOKEN": "your_token"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "gramps-mcp": {
      "command": "uvx",
      "args": ["--from", "gramps-mcp", "gramps-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "GRAMPS_WEB_URL": "https://service.example.com",
        "GRAMPS_WEB_TOKEN": "your_token"
      }
    }
  }
}
```

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`gramps-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/gramps-mcp/deployment/) has full,
copy-paste `mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://gramps-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Install Python Package

```bash
python -m pip install gramps-mcp
```

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/gramps-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)
