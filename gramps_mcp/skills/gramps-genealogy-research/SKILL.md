---
name: gramps-genealogy-research
skill_type: skill
description: >-
  Read genealogy from a Gramps tree via gramps-mcp: find people, families and life events, resolve kinship, walk timelines. Use to look up an ancestor by name or Gramps id, list family members, read birth/marriage/death events or compute a relationship. Do NOT use for KG ingestion (gramps-tree-ingestion) or photos (gramps-media-archive).
license: MIT
tags: [gramps, genealogy, people, families, events, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Gramps Genealogy Research

Scope: Genealogy research over a Gramps tree via the gramps-mcp MCP server — find and read people, families, and life events, resolve kinship, and walk a person's timeline. Use when the agent must look up an ancestor by name or Gramps id, list a family's members, read birth/marriage/death events, or compute the relationship between two people. Do NOT use to push the tree into the knowledge graph (use gramps-tree-ingestion) or to handle photos/scans (use gramps-media-archive).

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

## Steps

1. Find the person with `gramps_get_people` using `gramps_id` or a name filter and `profile=all`.
   Verify the result list contains the intended person.
2. Read the record with `gramps_get_person` (`handle`).
   Verify the `handle` and `gramps_id` match what the user asked for.
3. Read the family with `gramps_get_family` (`handle`) and `extend=child_ref_list,father_handle,mother_handle`.
   Verify father, mother and children are hydrated, not bare handles.
4. Read life events with `gramps_get_events` or the `event_ref_list` of the person.
   Verify each event carries a type and date before quoting it.
5. Resolve kinship with `gramps_get_relation` (`handle1`, `handle2`) or walk dates with `gramps_get_person_timeline` (`handle`).
   Verify the answer names both people.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| Not-found error for a handle | A `gramps_id` such as `I0042` was passed where the opaque `handle` is required, or the handle is from another tree | Resolve the record with the list tool and its `gramps_id` filter, then pass the `handle` it returns |
| Empty people list | Filter too strict or `gramps_id` mistyped | Loosen the `rules` filter or search with `gramps_get_search`, and confirm the id format such as `I0042` |
| Reference list returns bare handles | The read did not hydrate references | Repeat the read with `profile=all` and `extend` set, or read each handle with its typed tool |

## Tools
One typed tool per Gramps Web API operation, named `gramps_<operation>`; pass real arguments.

| Task | Tools |
|------|-------|
| People | `gramps_get_people`, `gramps_get_person`, `gramps_post_merge_person` |
| Families | `gramps_get_families`, `gramps_get_family`, `gramps_post_merge_family` |
| Events | `gramps_get_events`, `gramps_get_event`, `gramps_get_event_span` |
| Relationships | `gramps_get_relation`, `gramps_get_relations` |
| Timeline | `gramps_get_person_timeline`, `gramps_get_family_timeline` |
| Search | `gramps_get_search` |

Records are changed with `gramps_post_people`, `gramps_put_person`, `gramps_delete_person` (and the
same triple for families, events, places, citations, sources, repositories, media objects, notes
and tags). Writes need an editor-role account and approval; reads work with a guest account.

### Key parameters
- `handle` - the stable primary key for reading one person/family/event.
- Gramps list endpoints accept query params like `gramps_id`, `rules` (filter
  JSON), `page`, `pagesize`, and `keys`/`profile` to control returned fields.

## Recipes
Find a person by their Gramps id: `gramps_get_people` with `gramps_id=I0042`, `profile=all`.

Read one family and expand member profiles: `gramps_get_family` with `handle=<family_handle>`,
`profile=all`, `extend=child_ref_list,father_handle,mother_handle`.

List birth events: `gramps_get_events` with `rules={"rules":[{"name":"HasType","values":["Birth"]}]}`
(a JSON string) and `pagesize=25`.

## Gotchas
- Records are keyed by `handle` (opaque, stable); `gramps_id` (e.g. `I0042`) is the
  human-facing id and is what people usually quote.
- Relationships between objects are handles inside ref-lists
  (`event_ref_list:[{"ref":...}]`, `child_ref_list`, `father_handle`) — resolve them
  with a second read, or pass `extend`/`profile` to hydrate in one call.
- `gender` is an integer on the person record: `0`=female, `1`=male, `2`=unknown.

## Related
- **gramps-tree-ingestion** — push these same people/families/events into the KG.
- **gramps-media-archive** — the photos/scans attached to these records.
