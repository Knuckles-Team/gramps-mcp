---
name: gramps-genealogy-research
skill_type: skill
description: >-
  Genealogy research over a Gramps tree via the gramps-mcp MCP server — find and
  read people, families, and life events, resolve kinship, and walk a person's
  timeline. Use when the agent must look up an ancestor by name or Gramps id,
  list a family's members, read birth/marriage/death events, or compute the
  relationship between two people. Do NOT use to push the tree into the knowledge
  graph (use gramps-tree-ingestion) or to handle photos/scans (use
  gramps-media-archive).
license: MIT
tags: [gramps, genealogy, people, families, events, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Gramps Genealogy Research

Domain-typed read access to a **Gramps** genealogy database (people, families,
events, places, relations, timelines) through the gramps-mcp MCP server. Prefer
these tools over ad-hoc calls — they return Gramps-shaped records keyed by the
stable `handle`.

## When to use
- Find a person by name / `gramps_id`, or read one by `handle`.
- List a family's father, mother, and children.
- Read the events (birth, marriage, death, census) tied to a person or family.
- Compute the relationship / kinship path between two people.
- Walk a person's chronological timeline.

## When NOT to use
- Ingesting the tree as typed nodes into the knowledge graph → `gramps-tree-ingestion`.
- Photos, scans, face-detection, OCR of media → `gramps-media-archive`.
- Bulk exports (GEDCOM), imports, or destructive merges → use the raw
  `gramps_exporters` / `gramps_importers` / `*_merge_*` tools directly.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gramps-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `GRAMPS_URL` | ✅ | Gramps Web API base URL |
| `GRAMPS_TOKEN` | one-of | Pre-minted JWT bearer token |
| `GRAMPS_USERNAME` / `GRAMPS_PASSWORD` | one-of | Login exchanged at `/api/token/` |
| `GRAMPS_SSL_VERIFY` | optional | TLS verification toggle (default true) |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed action-routed
surface (used below) vs. the one-to-one verbose tools.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `gramps_people` | `get_people`, `get_person`, `post_merge_person` |
| `gramps_families` | `get_families`, `get_family`, `post_families`, `post_merge_family` |
| `gramps_events` | `get_events`, `get_event`, `get_event_span` |
| `gramps_relations` | relationship / kinship lookups between two people |
| `gramps_timeline` | per-person chronological timeline |
| `gramps_search` | full-text search across the tree |

### Key parameters
- `handle` — the stable primary key for reading one person/family/event.
- Gramps list endpoints accept query params like `gramps_id`, `rules` (filter
  JSON), `page`, `pagesize`, and `keys`/`profile` to control returned fields.

## Recipes (`params_json`)
Find a person by their Gramps id (`gramps_people`, action `get_people`):
```json
{"gramps_id":"I0042","profile":"all"}
```
Read one family and expand member profiles (`gramps_families`, `get_family`):
```json
{"handle":"<family_handle>","profile":"all","extend":"child_ref_list,father_handle,mother_handle"}
```
List birth/death events (`gramps_events`, `get_events`):
```json
{"rules":"{\"rules\":[{\"name\":\"HasType\",\"values\":[\"Birth\"]}]}","pagesize":25}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Records are keyed by `handle` (opaque, stable); `gramps_id` (e.g. `I0042`) is the
  human-facing id and is what people usually quote.
- Relationships between objects are handles inside ref-lists
  (`event_ref_list:[{"ref":...}]`, `child_ref_list`, `father_handle`) — resolve them
  with a second read, or pass `extend`/`profile` to hydrate in one call.
- `gender` is an integer on the person record: `0`=female, `1`=male, `2`=unknown.

## Related
- **gramps-tree-ingestion** — push these same people/families/events into the KG.
- **gramps-media-archive** — the photos/scans attached to these records.
