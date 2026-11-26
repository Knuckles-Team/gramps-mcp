---
name: gramps-media-archive
skill_type: skill
description: >-
  Work with media attached to a Gramps tree via gramps-mcp: list/read media objects, fetch file bytes, run face detection or OCR, and archive a file as a content-addressed :MediaAsset blob. Use to inspect, extract text from or archive genealogy images. Do NOT use for people, family or event records (gramps-genealogy-research or gramps-tree-ingestion).
license: MIT
tags: [gramps, genealogy, media, blob, ocr, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Gramps Media Archive

Scope: Work with the media (photos, scanned certificates, document images) attached to a Gramps tree via the gramps-mcp MCP server — list/read media objects, fetch file bytes, run face detection or OCR, and natively store a media file's raw bytes into the knowledge graph as a content-addressed :MediaAsset blob. Use when the agent must inspect, extract text from, or durably archive genealogy images. Do NOT use for people/family/event records (use gramps-genealogy-research or gramps-tree-ingestion).

Domain-typed access to **Gramps media objects** and their files through the
gramps-mcp MCP server, plus native blob ingestion: a media file's raw bytes are
stored as a content-addressed `:MediaAsset` blob in the medulla engine in
one cross-modal commit — the image itself, not just a path, becomes durable and
queryable.

## Steps

1. List media with `gramps_get_media_objects` and `pagesize=25`.
   Verify each entry has a `handle` and a `mime` value.
2. Read one object with `gramps_get_media_object` (`handle`).
   Verify the `gramps_id`, `path` and `checksum` are present.
3. Fetch bytes with `gramps_get_media_file` (`handle`) only when needed.
   Verify the response is raw file content with the expected `mime`, not JSON.
4. Run `gramps_post_media_ocr` (`handle`) for text or `gramps_get_media_face_detection` (`handle`) for faces.
   Verify the output is non-empty or report that none was found.
5. To archive durably, request arbora governed media sync, which reads through `gramps_get_media_file`.
   Verify the same checksum returns the existing asset instead of a duplicate.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| Not-found error for a handle | A `gramps_id` such as `I0042` was passed where the opaque `handle` is required, or the handle is from another tree | Resolve the record with the list tool and its `gramps_id` filter, then pass the `handle` it returns |
| Archive reports no-op | No reachable medulla engine for blob ingestion | Ask the operator to restore the engine connection through arbora, then repeat the sync request and check the asset appears |
| OCR returns empty text | Image is not a text scan or is low resolution | Confirm the `mime` and `path` with `gramps_get_media_object`, and report that no text was found rather than inventing it |

## When to use
- List / read media objects; fetch a media file's bytes.
- Run face detection or OCR against a scanned image.
- Durably archive a photo/scan into the knowledge graph as a `:MediaAsset` blob.

## When NOT to use
- People, families, events → `gramps-genealogy-research` / `gramps-tree-ingestion`.
- You only need the `:hasMedia` link, not the bytes → tree-ingestion already records it.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`gramps-mcp`** MCP server (same
`GRAMPS_URL` + token/login auth). Blob ingestion additionally needs a reachable
medulla engine; without one the media sync is a no-op.

## Tools
| Tool | Purpose |
|------|---------|
| `gramps_get_media_objects`, `gramps_get_media_object` | list / read media objects |
| `gramps_get_media_file`, `gramps_get_media_face_detection` | file bytes, face detection |
| `gramps_post_media_ocr`, `gramps_post_media_archive` | OCR, archive |

Storing a photo's bytes into the knowledge graph is done by arbora's governed media sync, which reads
through `gramps_get_media_file`.

### Key parameters
- `handle` - the media object's stable key (required to read the object, its file,
  face detection or OCR).

## Recipes
List media objects: `gramps_get_media_objects` with `pagesize=25`.

OCR a scanned certificate: `gramps_post_media_ocr` with `handle=<media_handle>`.

## Gotchas
- `gramps_get_media_file` returns the **raw file bytes** on the underlying HTTP
  response (`response.content`), not JSON; the media sync reads them from there.
- `media_type` is inferred from the object's `mime` (`image/*`→image, else file);
  most genealogy media are `image/jpeg` scans/photos.
- The blob is content-addressed (deduped by digest) — re-ingesting the same file
  returns the existing asset rather than duplicating bytes.
- Carried metadata on the `:MediaAsset`: `handle`, `gramps_id`, `path`, `mime`,
  `desc`, `checksum` (source=`gramps-mcp`).

## Related
- **gramps-tree-ingestion** — records the `:hasMedia` link from a person/event to
  the media handle this skill stores the bytes for.
- **gramps-genealogy-research** — the records these images document.
