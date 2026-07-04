---
name: gramps-tree-ingestion
description: >-
  Ingest a Gramps family tree natively into the epistemic-graph knowledge graph
  via the gramps-mcp MCP server — people become typed :Person nodes, families
  :Family nodes, and life events :Event nodes, wired by kinship
  (:hasFather/:hasMother/:hasChild) and participation (:participatedInEvent)
  links. Use when the agent must mirror or refresh a genealogy database into the
  KG for cross-source querying. Do NOT use for plain read/lookup (use
  gramps-genealogy-research) or for storing photo/scan bytes (use
  gramps-media-archive).
license: MIT
tags: [gramps, genealogy, knowledge-graph, ingestion, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Gramps Tree Ingestion

Native "maximum ingestion" of a Gramps tree into the ONE epistemic-graph engine.
The gramps-mcp server lists records and pushes them as **typed OWL nodes** matching
`gramps.ttl` (`:Person`, `:Family`, `:Event`) with their kinship and participation
links, via the fast engine client. Best-effort: with no reachable engine each tool
returns `{"ingested": null}` and nothing breaks.

## When to use
- Mirror or refresh an entire Gramps tree into the knowledge graph.
- Make people/families/events cross-queryable against other KG sources.
- Seed the graph before relationship reasoning across genealogy + other domains.

## When NOT to use
- One-off lookups / reading a single record → `gramps-genealogy-research`.
- Storing the raw bytes of a photo or scanned certificate → `gramps-media-archive`.
- You have no running epistemic-graph engine — ingestion no-ops by design.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gramps-mcp`** MCP server (same
`GRAMPS_URL` + `GRAMPS_TOKEN` / `GRAMPS_USERNAME`+`GRAMPS_PASSWORD` auth as the
research skill). A reachable epistemic-graph engine is required for a non-null
`ingested` result; without one the tools still return the `listed` count.

Node ids are deterministic — `gramps:<Class>:<handle>` — so re-ingesting the same
records MERGEs (upserts) rather than duplicating.

## Tools & actions
These are direct KG tools (no `action` router); each lists via the Gramps API and
pushes into the graph.

| Tool | Ingests | Argument |
|------|---------|----------|
| `gramps_ingest_people` | `:Person` (+ `:spouseInFamily`/`:childInFamily`/`:participatedInEvent`/`:hasMedia`) | `params_json` = get_people filters |
| `gramps_ingest_families` | `:Family` (+ `:hasFather`/`:hasMother`/`:hasChild`) | `params_json` = get_families filters |
| `gramps_ingest_events` | `:Event` (+ `:occurredAtPlace`) | `params_json` = get_events filters |

## Recipes
Ingest all people (default filters):
```json
{}
```
Ingest a paged slice of families (`gramps_ingest_families`, `params_json`):
```json
{"page":1,"pagesize":200}
```
Full refresh order: ingest **people**, then **families**, then **events** — so the
kinship edges from families/people resolve onto already-present nodes (edges are
best-effort and self-heal on re-ingest regardless of order).

## Gotchas
- Ingestion is **best-effort**: `{"ingested": null}` means no engine was reachable,
  not that listing failed — check the `listed` count.
- Ids are `gramps:<Class>:<handle>`; the `type` on each node matches a class in
  `gramps_mcp/ontology/gramps.ttl` (federated via the ontology entry-point).
- Photos are **not** pulled by these tools — they only record a `:hasMedia` link to
  the media handle. Use `gramps-media-archive` to store the actual bytes.
- Provenance `source=gramps-mcp` / `domain=gramps` is stamped on every node.

## Related
- **gramps-genealogy-research** — read the records these tools ingest.
- **gramps-media-archive** — store the blob bytes behind the `:hasMedia` links.
- The `agent-utilities-source-integration` skill drives generic `source_sync` presets
  (see `gramps_mcp/connectors/mcp_source_presets.json`).
