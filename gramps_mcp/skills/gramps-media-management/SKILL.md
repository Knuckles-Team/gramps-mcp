---
name: gramps-media-management
skill_type: skill
description: >-
  Manage media objects, their files, archives, face detection and OCR. Do NOT use for
  tasks outside the gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps media

Use the typed tools of the `gramps-mcp` connector: one tool per upstream API operation, named `gramps_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **gramps-people** (`GRAMPS_URL`): holds Person; read with `gramps_get_people`.
- **gramps-families** (`GRAMPS_URL`): holds Family; read with `gramps_get_families`.
- **gramps-events** (`GRAMPS_URL`): holds Event; read with `gramps_get_events`.
- **gramps-places** (`GRAMPS_URL`): holds Place; read with `gramps_get_places`.
- **gramps-sources** (`GRAMPS_URL`): holds Source; read with `gramps_get_sources`.
- **gramps-media** (`GRAMPS_URL`): holds MediaAsset; read with `gramps_get_media_objects`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `gramps-manage-object`

1. `gramps_get_media_object` (`handle`) - Get media object.
2. `gramps_get_media_objects` (no parameters) - Get media objects.
3. `gramps_post_media_objects` (`body`) - Post media objects.
4. `gramps_put_media_object` (`body`, `handle`) - Put media object.
5. `gramps_delete_media_object` (`confirm`, `handle`) - Delete media object. (destructive: ask the operator first)

### `gramps-manage-file`

1. `gramps_get_media_archive_filename` (`filename`) - Get media archive filename.
2. `gramps_get_media_file` (`handle`) - Get media file.
3. `gramps_post_media_archive` (`body`) - Post media archive.
4. `gramps_post_media_archive_upload_zip` (`body`) - Post media archive upload zip.
5. `gramps_put_media_file` (`body`, `handle`) - Put media file.

### `gramps-manage-analysis`

1. `gramps_get_media_face_detection` (`handle`) - Get media face detection.
2. `gramps_post_media_ocr` (`body`, `handle`) - Post media ocr.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
