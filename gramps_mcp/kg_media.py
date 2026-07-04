"""Native epistemic-graph blob ingestion for Gramps media (photos/scans).

CONCEPT:AU-KG.ingest.list-durable-media. A Gramps media object references a real file
(a photo, a scanned certificate, a document image). When a live epistemic-graph engine
is reachable, that file's raw bytes are stored as a content-addressed **blob** with a
``:MediaAsset`` graph node (carrying its Gramps metadata) in ONE cross-modal ACID commit
via the agent-utilities ``MediaStore`` — making the image itself, not just a path,
durable, deduped and queryable inside the knowledge graph.

The ``MediaStore`` is obtained through the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest.media_store`` when available, else
a guarded local fallback. Everything is dependency-/engine-guarded: with no KG stack or no
reachable engine every entry point **no-ops** (returns ``None``), so the connector runs
with zero KG infrastructure.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("gramps_mcp.kg_media")

_SOURCE = "gramps-mcp"

# Gramps media-object keys worth carrying onto the :MediaAsset node.
_MEDIA_FIELDS = ("handle", "gramps_id", "path", "mime", "desc", "checksum", "date")


def media_store() -> Any | None:
    """Return a ``MediaStore`` over a live engine, or ``None`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest.media_store()
    except Exception as e:  # noqa: BLE001 — primitive not installed yet
        logger.debug("KG media: shared primitive unavailable: %s", e)
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
        from agent_utilities.knowledge_graph.memory.media_store import MediaStore
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG media ingest unavailable (import): %s", e)
        return None
    try:
        engine = GraphComputeEngine()
        if getattr(engine, "_client", None) is None:
            return None
        return MediaStore(engine)
    except Exception as e:  # noqa: BLE001 — no reachable engine
        logger.debug("KG media ingest: engine unreachable: %s", e)
        return None


def ingest_media_blob(
    data: bytes | None,
    *,
    media: dict[str, Any] | None = None,
    mime_type: str | None = None,
    source: str = _SOURCE,
    store: Any | None = None,
) -> dict[str, Any] | None:
    """Store a Gramps media file's raw bytes as a blob + ``:MediaAsset``. Never raises.

    ``data``: the raw file bytes (from ``get_media_file``). ``media``: the Gramps media
    object dict (handle/gramps_id/path/mime/desc/checksum). Returns
    ``{asset_id, digest, size_bytes, media_type}`` on success, or ``None`` when there is
    no engine, no bytes, or the store failed. ``store`` may be injected (tests).
    """
    if not data:
        return None
    st = store if store is not None else media_store()
    if st is None:
        return None

    media = media or {}
    mime = mime_type or media.get("mime") or "application/octet-stream"
    if mime.startswith("image"):
        media_type = "image"
    elif mime.startswith("audio"):
        media_type = "audio"
    elif mime.startswith("video"):
        media_type = "video"
    else:
        media_type = "file"

    extra = {k: media[k] for k in _MEDIA_FIELDS if media.get(k) is not None}
    name = media.get("desc") or media.get("path") or media.get("gramps_id") or "media"

    try:
        stored = st.store_media(
            data,
            media_type=media_type,
            mime_type=mime,
            source=source,
            name=name,
            extra=extra,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("KG media ingest: store_media failed: %s", e)
        return None
    if stored is None:
        return None

    logger.info(
        "KG media ingest: stored %s (%s bytes) as asset %s",
        name,
        len(data),
        getattr(stored, "asset_id", "?"),
    )
    return {
        "asset_id": getattr(stored, "asset_id", None),
        "digest": getattr(stored, "digest", None),
        "size_bytes": len(data),
        "media_type": media_type,
    }
