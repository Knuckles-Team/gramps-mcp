---
name: gramps-family-records
skill_type: skill
description: >-
  Create, read, update and delete people, families, events and places. Do NOT use for
  tasks outside the gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps people, families, events and places

Use the typed tools of the `gramps-mcp` connector: one tool per upstream API operation, named `gramps_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Steps

1. Locate the person with `gramps_get_people` using a narrow filter and a small `pagesize`.
   Verify the result count is small enough to identify exactly one record.
2. Read the full record with `gramps_get_person` (`handle`).
   Verify the returned `handle` and `gramps_id` match the intended person.
3. For a new record, check for an existing duplicate with `gramps_get_people` before calling `gramps_post_people` (`body`).
   Verify no matching record already exists.
4. To change a record, state the exact fields to the operator, and call `gramps_put_person` (`body`, `handle`).
   Verify by re-reading with `gramps_get_person` that only those fields differ.
5. To remove a record, get explicit operator approval and call `gramps_delete_person` (`confirm`, `handle`) with `confirm=true`.
   Verify `gramps_get_person` for that `handle` now returns not-found.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| Not-found error for a handle | A `gramps_id` such as `I0042` was passed where the opaque `handle` is required, or the handle is from another tree | Resolve the record with the list tool and its `gramps_id` filter, then pass the `handle` it returns |
| Delete refused | `confirm=true` was not passed to `gramps_delete_person`, or the record is still referenced | Ask the operator for approval, pass `confirm=true`, and detach references from the referring records first |

## Where the data lives

- **gramps-people** (`GRAMPS_URL`): holds Person; read with `gramps_get_people`.
- **gramps-families** (`GRAMPS_URL`): holds Family; read with `gramps_get_families`.
- **gramps-events** (`GRAMPS_URL`): holds Event; read with `gramps_get_events`.
- **gramps-places** (`GRAMPS_URL`): holds Place; read with `gramps_get_places`.
- **gramps-sources** (`GRAMPS_URL`): holds Source; read with `gramps_get_sources`.
- **gramps-media** (`GRAMPS_URL`): holds MediaAsset; read with `gramps_get_media_objects`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `gramps-manage-event`

1. `gramps_get_event` (`handle`) - Get event.
2. `gramps_get_event_span` (`handle1`, `handle2`) - Get event span.
3. `gramps_get_events` (no parameters) - Get events.
4. `gramps_post_events` (`body`) - Post events.
5. `gramps_put_event` (`body`, `handle`) - Put event.
6. `gramps_delete_event` (`confirm`, `handle`) - Delete event. (destructive: ask the operator first)

### `gramps-manage-family`

1. `gramps_get_families` (no parameters) - Get families.
2. `gramps_get_family` (`handle`) - Get family.
3. `gramps_post_families` (`body`) - Post families.
4. `gramps_put_family` (`body`, `handle`) - Put family.
5. `gramps_delete_family` (`confirm`, `handle`) - Delete family. (destructive: ask the operator first)

### `gramps-manage-person`

1. `gramps_get_people` (no parameters) - Get people.
2. `gramps_get_person` (`handle`) - Get person.
3. `gramps_post_people` (`body`) - Post people.
4. `gramps_put_person` (`body`, `handle`) - Put person.
5. `gramps_delete_person` (`confirm`, `handle`) - Delete person. (destructive: ask the operator first)

### `gramps-manage-place`

1. `gramps_get_place` (`handle`) - Get place.
2. `gramps_get_places` (no parameters) - Get places.
3. `gramps_post_places` (`body`) - Post places.
4. `gramps_put_place` (`body`, `handle`) - Put place.
5. `gramps_delete_place` (`confirm`, `handle`) - Delete place. (destructive: ask the operator first)

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
