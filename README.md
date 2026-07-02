# Gramps MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/gramps-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/gramps-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gramps-mcp)
![PyPI - License](https://img.shields.io/pypi/l/gramps-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gramps-mcp)

*Version: 1.0.0*

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

**Gramps MCP MCP Server + A2A Agent**

Gramps API + MCP Server + A2A Agent — genealogy (people/families/events/places/sources/media)

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
| `gramps_bookmarks` | `BOOKMARKSTOOL` | Manage Gramps bookmarks operations. CONCEPT:GRMP-001. |
| `gramps_chat` | `CHATTOOL` | Manage Gramps chat operations. CONCEPT:GRMP-001. |
| `gramps_citations` | `CITATIONSTOOL` | Manage Gramps citations operations. CONCEPT:GRMP-001. |
| `gramps_config` | `CONFIGTOOL` | Manage Gramps config operations. CONCEPT:GRMP-001. |
| `gramps_dna` | `DNATOOL` | Manage Gramps dna operations. CONCEPT:GRMP-001. |
| `gramps_events` | `EVENTSTOOL` | Manage Gramps events operations. CONCEPT:GRMP-001. |
| `gramps_exporters` | `EXPORTERSTOOL` | Manage Gramps exporters operations. CONCEPT:GRMP-001. |
| `gramps_facts` | `FACTSTOOL` | Manage Gramps facts operations. CONCEPT:GRMP-001. |
| `gramps_families` | `FAMILIESTOOL` | Manage Gramps families operations. CONCEPT:GRMP-001. |
| `gramps_filters` | `FILTERSTOOL` | Manage Gramps filters operations. CONCEPT:GRMP-001. |
| `gramps_holidays` | `HOLIDAYSTOOL` | Manage Gramps holidays operations. CONCEPT:GRMP-001. |
| `gramps_importers` | `IMPORTERSTOOL` | Manage Gramps importers operations. CONCEPT:GRMP-001. |
| `gramps_living` | `LIVINGTOOL` | Manage Gramps living operations. CONCEPT:GRMP-001. |
| `gramps_media` | `MEDIATOOL` | Manage Gramps media operations. CONCEPT:GRMP-001. |
| `gramps_metadata` | `METADATATOOL` | Manage Gramps metadata operations. CONCEPT:GRMP-001. |
| `gramps_name_formats` | `NAME_FORMATSTOOL` | Manage Gramps name formats operations. CONCEPT:GRMP-001. |
| `gramps_name_groups` | `NAME_GROUPSTOOL` | Manage Gramps name groups operations. CONCEPT:GRMP-001. |
| `gramps_notes` | `NOTESTOOL` | Manage Gramps notes operations. CONCEPT:GRMP-001. |
| `gramps_oidc` | `OIDCTOOL` | Manage Gramps oidc operations. CONCEPT:GRMP-001. |
| `gramps_people` | `PEOPLETOOL` | Manage Gramps people operations. CONCEPT:GRMP-001. |
| `gramps_places` | `PLACESTOOL` | Manage Gramps places operations. CONCEPT:GRMP-001. |
| `gramps_relations` | `RELATIONSTOOL` | Manage Gramps relations operations. CONCEPT:GRMP-001. |
| `gramps_reports` | `REPORTSTOOL` | Manage Gramps reports operations. CONCEPT:GRMP-001. |
| `gramps_repositories` | `REPOSITORIESTOOL` | Manage Gramps repositories operations. CONCEPT:GRMP-001. |
| `gramps_search` | `SEARCHTOOL` | Manage Gramps search operations. CONCEPT:GRMP-001. |
| `gramps_sources` | `SOURCESTOOL` | Manage Gramps sources operations. CONCEPT:GRMP-001. |
| `gramps_tags` | `TAGSTOOL` | Manage Gramps tags operations. CONCEPT:GRMP-001. |
| `gramps_tasks` | `TASKSTOOL` | Manage Gramps tasks operations. CONCEPT:GRMP-001. |
| `gramps_timeline` | `TIMELINETOOL` | Manage Gramps timeline operations. CONCEPT:GRMP-001. |
| `gramps_token` | `TOKENTOOL` | Manage Gramps token operations. CONCEPT:GRMP-001. |
| `gramps_transactions` | `TRANSACTIONSTOOL` | Manage Gramps transactions operations. CONCEPT:GRMP-001. |
| `gramps_translations` | `TRANSLATIONSTOOL` | Manage Gramps translations operations. CONCEPT:GRMP-001. |
| `gramps_trees` | `TREESTOOL` | Manage Gramps trees operations. CONCEPT:GRMP-001. |
| `gramps_types` | `TYPESTOOL` | Manage Gramps types operations. CONCEPT:GRMP-001. |
| `gramps_users` | `USERSTOOL` | Manage Gramps users operations. CONCEPT:GRMP-001. |

_35 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `gramps-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `gramps-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated A2A agent** |
| `gramps-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "gramps-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "gramps-mcp[agent]"

# Everything (development)
uv pip install "gramps-mcp[all]"      # or: python -m pip install "gramps-mcp[all]"
```

### Install with `uvx` (no install — run on demand)

```bash
uvx --from "gramps-mcp[mcp]" gramps-mcp      # MCP server (slim)
uvx --from "gramps-mcp[agent]" gramps-agent  # A2A agent server (full runtime)
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/gramps-mcp:mcp` | `--target mcp` | `gramps-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `gramps-mcp` |
| `knucklessg1/gramps-mcp:latest` | `--target agent` (default) | `gramps-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `gramps-agent` |

```bash
docker build --target mcp   -t knucklessg1/gramps-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/gramps-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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

> **Install the slim `[mcp]` extra.** The MCP examples below install
> `gramps-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP / FastAPI
> tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy agent
> runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated A2A agent
> (see [Installation](#installation)).

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the slim `[mcp]` extra.** All examples install `gramps-mcp[mcp]` — the
> MCP-server extra that pulls only the FastMCP / FastAPI tooling (`agent-utilities[mcp]`).
> It deliberately **excludes** the heavy agent runtime (`pydantic-ai`, the epistemic-graph
> engine, `dspy`, `llama-index`), so `uvx` / container installs are far smaller. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "gramps-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "gramps-mcp[mcp]",
        "gramps-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "BOOKMARKSTOOL": "True",
        "CHATTOOL": "True",
        "CITATIONSTOOL": "True",
        "CONFIGTOOL": "True",
        "DNATOOL": "True",
        "EVENTSTOOL": "True",
        "EXPORTERSTOOL": "True",
        "FACTSTOOL": "True",
        "FAMILIESTOOL": "True",
        "FILTERSTOOL": "True",
        "GRAMPS_PASSWORD": "your_password_here",
        "GRAMPS_TOKEN": "your_jwt_here",
        "GRAMPS_URL": "https://gramps.arpa",
        "GRAMPS_USERNAME": "owner",
        "HOLIDAYSTOOL": "True",
        "IMPORTERSTOOL": "True",
        "LIVINGTOOL": "True",
        "MEDIATOOL": "True",
        "METADATATOOL": "True",
        "NAME_FORMATSTOOL": "True",
        "NAME_GROUPSTOOL": "True",
        "NOTESTOOL": "True",
        "OIDCTOOL": "True",
        "PEOPLETOOL": "True",
        "PLACESTOOL": "True",
        "RELATIONSTOOL": "True",
        "REPORTSTOOL": "True",
        "REPOSITORIESTOOL": "True",
        "SEARCHTOOL": "True",
        "SOURCESTOOL": "True",
        "TAGSTOOL": "True",
        "TASKSTOOL": "True",
        "TIMELINETOOL": "True",
        "TOKENTOOL": "True",
        "TRANSACTIONSTOOL": "True",
        "TRANSLATIONSTOOL": "True",
        "TREESTOOL": "True",
        "TYPESTOOL": "True",
        "USERSTOOL": "True"
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
      "args": [
        "--from",
        "gramps-mcp[mcp]",
        "gramps-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MCP_TOOL_MODE": "condensed",
        "BOOKMARKSTOOL": "True",
        "CHATTOOL": "True",
        "CITATIONSTOOL": "True",
        "CONFIGTOOL": "True",
        "DNATOOL": "True",
        "EVENTSTOOL": "True",
        "EXPORTERSTOOL": "True",
        "FACTSTOOL": "True",
        "FAMILIESTOOL": "True",
        "FILTERSTOOL": "True",
        "GRAMPS_PASSWORD": "your_password_here",
        "GRAMPS_TOKEN": "your_jwt_here",
        "GRAMPS_URL": "https://gramps.arpa",
        "GRAMPS_USERNAME": "owner",
        "HOLIDAYSTOOL": "True",
        "IMPORTERSTOOL": "True",
        "LIVINGTOOL": "True",
        "MEDIATOOL": "True",
        "METADATATOOL": "True",
        "NAME_FORMATSTOOL": "True",
        "NAME_GROUPSTOOL": "True",
        "NOTESTOOL": "True",
        "OIDCTOOL": "True",
        "PEOPLETOOL": "True",
        "PLACESTOOL": "True",
        "RELATIONSTOOL": "True",
        "REPORTSTOOL": "True",
        "REPOSITORIESTOOL": "True",
        "SEARCHTOOL": "True",
        "SOURCESTOOL": "True",
        "TAGSTOOL": "True",
        "TASKSTOOL": "True",
        "TIMELINETOOL": "True",
        "TOKENTOOL": "True",
        "TRANSACTIONSTOOL": "True",
        "TRANSLATIONSTOOL": "True",
        "TREESTOOL": "True",
        "TYPESTOOL": "True",
        "USERSTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "gramps-mcp": {
      "url": "http://localhost:8000/gramps-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name gramps-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e MCP_TOOL_MODE=condensed \
  -e BOOKMARKSTOOL=True \
  -e CHATTOOL=True \
  -e CITATIONSTOOL=True \
  -e CONFIGTOOL=True \
  -e DNATOOL=True \
  -e EVENTSTOOL=True \
  -e EXPORTERSTOOL=True \
  -e FACTSTOOL=True \
  -e FAMILIESTOOL=True \
  -e FILTERSTOOL=True \
  -e GRAMPS_PASSWORD=your_password_here \
  -e GRAMPS_TOKEN=your_jwt_here \
  -e GRAMPS_URL=https://gramps.arpa \
  -e GRAMPS_USERNAME=owner \
  -e HOLIDAYSTOOL=True \
  -e IMPORTERSTOOL=True \
  -e LIVINGTOOL=True \
  -e MEDIATOOL=True \
  -e METADATATOOL=True \
  -e NAME_FORMATSTOOL=True \
  -e NAME_GROUPSTOOL=True \
  -e NOTESTOOL=True \
  -e OIDCTOOL=True \
  -e PEOPLETOOL=True \
  -e PLACESTOOL=True \
  -e RELATIONSTOOL=True \
  -e REPORTSTOOL=True \
  -e REPOSITORIESTOOL=True \
  -e SEARCHTOOL=True \
  -e SOURCESTOOL=True \
  -e TAGSTOOL=True \
  -e TASKSTOOL=True \
  -e TIMELINETOOL=True \
  -e TOKENTOOL=True \
  -e TRANSACTIONSTOOL=True \
  -e TRANSLATIONSTOOL=True \
  -e TREESTOOL=True \
  -e TYPESTOOL=True \
  -e USERSTOOL=True \
  knucklessg1/gramps-mcp:mcp
```

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

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

## Environment Variables

Every variable the server reads, grouped by purpose.

### Connection & Credentials (Gramps)
| Variable | Description | Default |
|----------|-------------|---------|
| `GRAMPS_URL` | Base Gramps Web API URL | `https://gramps.arpa` |
| `GRAMPS_TOKEN` | JWT bearer token (from the login flow) | — |
| `GRAMPS_USERNAME` | Username for the login flow (when no token) | — |
| `GRAMPS_PASSWORD` | Password for the login flow (when no token) | — |
| `GRAMPS_SSL_VERIFY` | TLS verification | `True` |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `both` |

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above (e.g.
`PEOPLETOOL`, `FAMILIESTOOL`, `EVENTSTOOL`, `PLACESTOOL`, `SOURCESTOOL`, `MEDIATOOL`).

See [`.env.example`](.env.example) for a copy-paste starting point.

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/gramps-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)
