"""Native epistemic-graph media-blob ingestion — Wire-First coverage.

Exercises the real ``ingest_media_blob`` seam with a fake ``MediaStore`` (no engine
required), asserting the store_media call and the Gramps-media -> :MediaAsset mapping.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from dataclasses import dataclass

from gramps_mcp.kg_media import ingest_media_blob


@dataclass
class _Stored:
    asset_id: str
    digest: str


class _FakeMediaStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, **kw):
        self.calls.append((data, kw))
        return _Stored(asset_id="gramps:media:deadbeef", digest="deadbeef")


def test_ingest_media_blob_stores_bytes_and_metadata():
    store = _FakeMediaStore()
    res = ingest_media_blob(
        b"\xff\xd8jpeg-bytes",
        media={
            "handle": "M1",
            "gramps_id": "O0003",
            "path": "photos/grandpa.jpg",
            "mime": "image/jpeg",
            "desc": "Grandpa 1920",
            "checksum": "abc",
        },
        store=store,
    )
    assert res is not None
    assert res["asset_id"] == "gramps:media:deadbeef"
    assert res["digest"] == "deadbeef"
    assert res["media_type"] == "image"
    assert res["size_bytes"] == len(b"\xff\xd8jpeg-bytes")

    assert len(store.calls) == 1
    data, kw = store.calls[0]
    assert data == b"\xff\xd8jpeg-bytes"
    assert kw["source"] == "gramps-mcp"
    assert kw["mime_type"] == "image/jpeg"
    assert kw["media_type"] == "image"
    assert kw["name"] == "Grandpa 1920"
    assert kw["extra"]["handle"] == "M1"
    assert kw["extra"]["gramps_id"] == "O0003"


def test_ingest_media_blob_defaults_mime_and_name():
    store = _FakeMediaStore()
    res = ingest_media_blob(b"x", media={"gramps_id": "O0009"}, store=store)
    assert res["media_type"] == "file"
    _, kw = store.calls[0]
    assert kw["mime_type"] == "application/octet-stream"
    assert kw["name"] == "O0009"


def test_ingest_media_blob_noops_without_engine():
    # No injected store + no reachable engine -> clean no-op.
    assert ingest_media_blob(b"x") is None


def test_ingest_media_blob_noops_on_empty_bytes():
    assert ingest_media_blob(b"", store=_FakeMediaStore()) is None
    assert ingest_media_blob(None, store=_FakeMediaStore()) is None
