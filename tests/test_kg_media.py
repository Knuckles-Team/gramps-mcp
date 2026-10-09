"""Native epistemic-graph media-blob ingestion — Wire-First coverage.

Exercises the real ``ingest_media_blob`` seam against a fake SDK transport (no engine
required), asserting the ``store_blob``/``submit`` calls and the Gramps-media ->
:MediaAsset mapping. CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

import hashlib
from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from gramps_mcp.kg_media import ingest_media_blob


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []
        self.stored: list[bytes] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        self.stored.append(data)
        return hashlib.sha256(data).hexdigest()


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


async def test_ingest_media_blob_stores_bytes_and_metadata(ingest):
    service, transport = ingest
    data = b"\xff\xd8jpeg-bytes"
    res = await ingest_media_blob(
        data,
        media={
            "handle": "M1",
            "gramps_id": "O0003",
            "path": "photos/grandpa.jpg",
            "mime": "image/jpeg",
            "desc": "Grandpa 1920",
            "checksum": "abc",
        },
        ingest=service,
    )
    digest = hashlib.sha256(data).hexdigest()
    assert res is not None
    assert res["asset_id"] == f"blob:{digest}"
    assert res["digest"] == digest
    assert res["media_type"] == "image"
    assert res["size_bytes"] == len(data)

    assert transport.stored == [data]
    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "image/jpeg"
    assert record.payload["name"] == "Grandpa 1920"
    assert record.payload["handle"] == "M1"
    assert record.payload["gramps_id"] == "O0003"


async def test_ingest_media_blob_defaults_mime_and_name(ingest):
    service, transport = ingest
    res = await ingest_media_blob(b"x", media={"gramps_id": "O0009"}, ingest=service)
    assert res is not None
    assert res["media_type"] == "file"
    record = transport.requests[0].records[0]
    assert record.payload["mime_type"] == "application/octet-stream"
    assert record.payload["name"] == "O0009"


async def test_ingest_media_blob_noops_without_engine():
    # No injected ingest + no reachable engine -> clean no-op.
    assert await ingest_media_blob(b"x") is None


async def test_ingest_media_blob_noops_on_empty_bytes(ingest):
    service, _transport = ingest
    assert await ingest_media_blob(b"", ingest=service) is None
    assert await ingest_media_blob(None, ingest=service) is None
