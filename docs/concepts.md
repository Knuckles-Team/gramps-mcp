# Concept Registry — gramps-mcp

> **Prefix**: `CONCEPT:GRMP-*`
> **Version**: 0.1.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:GM-OS.identity.grmp` | Genealogy Connector | Action-routed + verbose 1:1 MCP tool surface over the Gramps REST API (people, families, events, places, sources, citations, media, notes, repositories, tags, trees, users, transactions, search, reports, importers/exporters, relations, timelines, DNA, …), generated from the vendored OpenAPI spec by `scripts/generate_from_openapi.py` |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
