"""Native epistemic-graph blob ingestion for Gramps media (photos/scans).

CONCEPT:AU-KG.ingest.list-durable-media. A Gramps media object references a real file
(a photo, a scanned certificate, a document image). When a live epistemic-graph engine
is reachable, that file's raw bytes are stored as a content-addressed **blob** with a
``:MediaAsset`` graph node (carrying its Gramps metadata) in ONE cross-modal ACID commit
via the ``agent_connector_sdk.ingest`` facade — making the image itself, not just a
path, durable, deduped and queryable inside the knowledge graph.

The knowledge-ingest service is obtained through ``agent_connector_sdk.ingest
.current_ingest()`` (process-installed, or connected from settings on first use).
Everything is dependency-/engine-guarded: with no KG stack or no reachable engine every
entry point **no-ops** (returns ``None``), so the connector runs with zero KG
infrastructure.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    IngestBinding,
    IngestError,
    IngestUnavailableError,
    KnowledgeIngest,
    MediaAsset,
    current_ingest,
)

logger = logging.getLogger("gramps_mcp.kg_media")

_BINDING = IngestBinding(connector="gramps-mcp", stream="gramps-media")

# Gramps media-object keys worth carrying onto the :MediaAsset node.
_MEDIA_FIELDS = ("handle", "gramps_id", "path", "mime", "desc", "checksum", "date")


def _media_type_for(mime: str) -> str:
    if mime.startswith("image"):
        return "image"
    if mime.startswith("audio"):
        return "audio"
    if mime.startswith("video"):
        return "video"
    return "file"


def _media_extra_fields(media: dict[str, Any]) -> dict[str, Any]:
    return {k: media[k] for k in _MEDIA_FIELDS if media.get(k) is not None}


def _media_display_name(media: dict[str, Any]) -> str:
    return media.get("desc") or media.get("path") or media.get("gramps_id") or "media"


async def ingest_media_blob(
    data: bytes | None,
    *,
    media: dict[str, Any] | None = None,
    mime_type: str | None = None,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store a Gramps media file's raw bytes as a blob + ``:MediaAsset``. Never raises.

    ``data``: the raw file bytes (from ``get_media_file``). ``media``: the Gramps media
    object dict (handle/gramps_id/path/mime/desc/checksum). Returns
    ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None`` when there is
    no engine, no bytes, or the store failed. ``ingest`` may be injected (tests).

    ``digest`` is computed client-side (SHA-256 of ``data``) for the caller's immediate
    use; it is the same content-addressing the engine's blob store uses, so it matches
    the asset id the engine derives when no explicit id is set.
    """
    if not data:
        return None

    media = media or {}
    mime = mime_type or media.get("mime") or "application/octet-stream"
    media_type = _media_type_for(mime)
    extra = _media_extra_fields(media)
    name = _media_display_name(media)
    digest = hashlib.sha256(data).hexdigest()

    asset = MediaAsset(data=data, mime_type=mime, name=name, properties=extra)
    change_set = ChangeSet(media=(asset,))
    try:
        service = ingest if ingest is not None else current_ingest()
        await service.submit(_BINDING, change_set)
    except (IngestError, IngestUnavailableError) as exc:
        logger.debug("KG media ingest unavailable/failed: %s", exc)
        return None

    logger.info("KG media ingest: stored %s (%s bytes) digest=%s", name, len(data), digest)
    return {
        "asset_id": f"blob:{digest}",
        "digest": digest,
        "size_bytes": len(data),
        "media_type": media_type,
    }
