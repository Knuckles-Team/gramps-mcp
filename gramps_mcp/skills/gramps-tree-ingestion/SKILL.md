---
name: gramps-tree-ingestion
skill_type: skill
description: >-
  Ingest a Gramps tree into the medulla knowledge graph via gramps-mcp: people, families and events become typed :Person, :Family and :Event nodes with kinship links. Use to mirror or refresh a genealogy database in the KG. Do NOT use for plain lookups (gramps-genealogy-research) or photo bytes (gramps-media-archive).
license: MIT
tags: [gramps, genealogy, knowledge-graph, ingestion, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Gramps Tree Ingestion

Scope: Ingest a Gramps family tree natively into the medulla knowledge graph via the gramps-mcp MCP server — people become typed :Person nodes, families :Family nodes, and life events :Event nodes, wired by kinship (:hasFather/:hasMother/:hasChild) and participation (:participatedInEvent) links. Use when the agent must mirror or refresh a genealogy database into the KG for cross-source querying. Do NOT use for plain read/lookup (use gramps-genealogy-research) or for storing photo/scan bytes (use gramps-media-archive).

Native "maximum ingestion" of a Gramps tree into the ONE medulla engine.
The gramps-mcp server lists records and pushes them as **typed OWL nodes** matching
`gramps.ttl` (`:Person`, `:Family`, `:Event`) with their kinship and participation
links, via the fast engine client. Best-effort: with no reachable engine each tool
returns `{"ingested": null}` and nothing breaks.

## Steps

1. Confirm the tree is reachable with `gramps_get_people` and `pagesize=1`.
   Verify one record returns with a `handle`.
2. Request arbora `source_sync` for the connector sources rather than pushing records by hand.
   Verify the request is accepted and returns a run reference.
3. Order a full refresh as `gramps_get_people`, followed by `gramps_get_families` and finally `gramps_get_events`, paging with `page` and `pagesize`.
   Verify the `listed` counts are non-zero for each.
4. Check the result field `ingested` for each source.
   Verify it is a number, and treat `null` as no reachable engine.
5. Spot-check one node with the id pattern `gramps:Person:<handle>`.
   Verify it exists once, so re-ingesting merged rather than duplicated.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| `ingested` is null | No reachable medulla engine, listing still worked | Ask the operator to restore the engine through arbora and repeat the `source_sync` request, then check `ingested` is a number |
| Kinship edges missing | Families or events ingested before people | Request `source_sync` again in the order people, families, events; edges self-heal on re-ingest |

## When to use
- Mirror or refresh an entire Gramps tree into the knowledge graph.
- Make people/families/events cross-queryable against other KG sources.
- Seed the graph before relationship reasoning across genealogy + other domains.

## When NOT to use
- One-off lookups / reading a single record → `gramps-genealogy-research`.
- Storing the raw bytes of a photo or scanned certificate → `gramps-media-archive`.
- You have no running medulla engine — ingestion no-ops by design.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gramps-mcp`** MCP server (same
`GRAMPS_URL` + `GRAMPS_TOKEN` / `GRAMPS_USERNAME`+`GRAMPS_PASSWORD` auth as the
research skill). A reachable medulla engine is required for a non-null
`ingested` result; without one the tools still return the `listed` count.

Node ids are deterministic — `gramps:<Class>:<handle>` — so re-ingesting the same
records MERGEs (upserts) rather than duplicating.

## Tools
Ingestion is arbora's governed sync of the connector's declared data sources, reading through
typed tools. Request it from arbora (`source_sync`); do not push records by hand.

| Source tool | Ingests |
|-------------|---------|
| `gramps_get_people` | `:Person` (+ `:spouseInFamily`/`:childInFamily`/`:participatedInEvent`/`:hasMedia`) |
| `gramps_get_families` | `:Family` (+ `:hasFather`/`:hasMother`/`:hasChild`) |
| `gramps_get_events` | `:Event` (+ `:occurredAtPlace`) |

Page with `page` and `pagesize`. Full refresh order: people, then families, then events, so the
kinship edges resolve onto already-present nodes (edges self-heal on re-ingest regardless of order).

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
- The `scion-sdk-source-integration` skill drives generic `source_sync` presets
  (see `gramps_mcp/connectors/mcp_source_presets.json`).
