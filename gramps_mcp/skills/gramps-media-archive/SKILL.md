---
name: gramps-media-archive
skill_type: skill
description: >-
  Work with the media (photos, scanned certificates, document images) attached to
  a Gramps tree via the gramps-mcp MCP server — list/read media objects, fetch
  file bytes, run face detection or OCR, and natively store a media file's raw
  bytes into the knowledge graph as a content-addressed :MediaAsset blob. Use when
  the agent must inspect, extract text from, or durably archive genealogy images.
  Do NOT use for people/family/event records (use gramps-genealogy-research or
  gramps-tree-ingestion).
license: MIT
tags: [gramps, genealogy, media, blob, ocr, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Gramps Media Archive

Domain-typed access to **Gramps media objects** and their files through the
gramps-mcp MCP server, plus native blob ingestion: a media file's raw bytes are
stored as a content-addressed `:MediaAsset` blob in the epistemic-graph engine in
one cross-modal commit — the image itself, not just a path, becomes durable and
queryable.

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
epistemic-graph engine; without one `gramps_ingest_media` no-ops (`{"ingested": null}`).

## Tools & actions
| Tool | Purpose |
|------|---------|
| `gramps_media` (condensed) | `get_media_objects`, `get_media_object`, `get_media_file`, `get_media_face_detection`, `post_media_ocr`, archive ops |
| `gramps_ingest_media` | fetch one media file's bytes + metadata and store it as a `:MediaAsset` blob (arg: `handle`) |

### Key parameters
- `handle` — the media object's stable key (required to read the object, its file,
  face detection, OCR, or to ingest its bytes).

## Recipes
List media objects (`gramps_media`, action `get_media_objects`, `params_json`):
```json
{"pagesize":25}
```
OCR a scanned certificate (`gramps_media`, action `post_media_ocr`):
```json
{"handle":"<media_handle>"}
```
Archive a photo's bytes into the KG (`gramps_ingest_media`):
```json
{"handle":"<media_handle>"}
```

## Gotchas
- `gramps_media get_media_file` returns the **raw file bytes** on the underlying HTTP
  response (`response.content`), not JSON — `gramps_ingest_media` reads them from there.
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
