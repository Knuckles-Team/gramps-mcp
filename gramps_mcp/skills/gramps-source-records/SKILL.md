---
name: gramps-source-records
skill_type: skill
description: >-
  Maintain sources, citations, repositories, notes and tags that back each fact. Do NOT
  use for tasks outside the gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps sources and notes

Use the typed tools of the `gramps-mcp` connector: one tool per upstream API operation, named `gramps_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Steps

1. Locate the source with `gramps_get_sources` using a narrow filter and a small `pagesize`.
   Verify the result count is small enough to identify exactly one record.
2. Read the full record with `gramps_get_source` (`handle`).
   Verify the returned `handle` and `gramps_id` match the intended source.
3. For a new record, check for an existing duplicate with `gramps_get_sources` before calling `gramps_post_sources` (`body`).
   Verify no matching record already exists.
4. To change a record, state the exact fields to the operator, and call `gramps_put_source` (`body`, `handle`).
   Verify by re-reading with `gramps_get_source` that only those fields differ.
5. To remove a record, get explicit operator approval and call `gramps_delete_source` (`confirm`, `handle`) with `confirm=true`.
   Verify `gramps_get_source` for that `handle` now returns not-found.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| Not-found error for a handle | A `gramps_id` such as `I0042` was passed where the opaque `handle` is required, or the handle is from another tree | Resolve the record with the list tool and its `gramps_id` filter, then pass the `handle` it returns |
| Delete refused | `confirm=true` was not passed to `gramps_delete_source`, or the record is still referenced | Ask the operator for approval, pass `confirm=true`, and detach references from the referring records first |

## Where the data lives

- **gramps-people** (`GRAMPS_URL`): holds Person; read with `gramps_get_people`.
- **gramps-families** (`GRAMPS_URL`): holds Family; read with `gramps_get_families`.
- **gramps-events** (`GRAMPS_URL`): holds Event; read with `gramps_get_events`.
- **gramps-places** (`GRAMPS_URL`): holds Place; read with `gramps_get_places`.
- **gramps-sources** (`GRAMPS_URL`): holds Source; read with `gramps_get_sources`.
- **gramps-media** (`GRAMPS_URL`): holds MediaAsset; read with `gramps_get_media_objects`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `gramps-manage-citation`

1. `gramps_get_citation` (`handle`) - Get citation.
2. `gramps_get_citations` (no parameters) - Get citations.
3. `gramps_post_citations` (`body`) - Post citations.
4. `gramps_put_citation` (`body`, `handle`) - Put citation.
5. `gramps_delete_citation` (`confirm`, `handle`) - Delete citation. (destructive: ask the operator first)

### `gramps-manage-note`

1. `gramps_get_note` (`handle`) - Get note.
2. `gramps_get_notes` (no parameters) - Get notes.
3. `gramps_post_notes` (`body`) - Post notes.
4. `gramps_put_note` (`body`, `handle`) - Put note.
5. `gramps_delete_note` (`confirm`, `handle`) - Delete note. (destructive: ask the operator first)

### `gramps-manage-repository`

1. `gramps_get_repositories` (no parameters) - Get repositories.
2. `gramps_get_repository` (`handle`) - Get repository.
3. `gramps_post_repositories` (`body`) - Post repositories.
4. `gramps_put_repository` (`body`, `handle`) - Put repository.
5. `gramps_delete_repository` (`confirm`, `handle`) - Delete repository. (destructive: ask the operator first)

### `gramps-manage-source`

1. `gramps_get_source` (`handle`) - Get source.
2. `gramps_get_sources` (no parameters) - Get sources.
3. `gramps_post_sources` (`body`) - Post sources.
4. `gramps_put_source` (`body`, `handle`) - Put source.
5. `gramps_delete_source` (`confirm`, `handle`) - Delete source. (destructive: ask the operator first)

### `gramps-manage-tag`

1. `gramps_get_tag` (`handle`) - Get tag.
2. `gramps_get_tags` (no parameters) - Get tags.
3. `gramps_post_tags` (`body`) - Post tags.
4. `gramps_put_tag` (`body`, `handle`) - Put tag.
5. `gramps_delete_tag` (`confirm`, `handle`) - Delete tag. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
