"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_people`` / ``ingest_families`` /
``ingest_events`` seam against a fake SDK transport (no engine required), asserting
the submitted records/relationships and the Gramps record -> typed-node mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.

Unlike most fleet connectors, ``gramps_mcp.kg_ingest`` is a **best-effort** surface
(its MCP tools must never raise when the KG stack is down), so it converts
``IngestError``/``IngestUnavailableError`` into ``None`` rather than propagating it —
those semantics are exercised explicitly below.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from gramps_mcp.kg_ingest import (
    ingest_entities,
    ingest_events,
    ingest_families,
    ingest_people,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: Any) -> Any:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Person", "name": "p"},
            {"id": "b", "node_type": "Family"},
        ],
        [{"source": "a", "target": "b", "relationship": "spouseInFamily"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    record_ids = {r.record_id for r in transport.requests[0].records}
    assert record_ids == {"a", "b"}
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "a"
    assert rel.target.record_id == "b"


async def test_ingest_people_maps_person_and_links(ingest):
    service, transport = ingest
    res = await ingest_people(
        [
            {
                "handle": "H1",
                "gramps_id": "I0042",
                "gender": 1,
                "primary_name": {
                    "first_name": "John",
                    "surname_list": [{"surname": "Doe"}],
                },
                "family_list": ["F1"],
                "parent_family_list": ["F0"],
                "event_ref_list": [{"ref": "E1"}],
                "media_list": [{"ref": "M1"}],
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 4}
    node = transport.requests[0].records[0]
    assert node.record_id == "gramps:Person:H1"
    assert node.payload["name"] == "John Doe"
    assert node.payload["gender"] == "male"
    assert node.payload["grampsId"] == "I0042"
    assert node.payload["externalToolId"] == "H1"
    edge_targets = {r.target.record_id for r in transport.requests[0].relationships}
    assert edge_targets == {
        "gramps:Family:F1",
        "gramps:Family:F0",
        "gramps:Event:E1",
        "gramps:MediaAsset:M1",
    }
    spouse_edge = next(
        r
        for r in transport.requests[0].relationships
        if r.target.record_id == "gramps:Family:F1"
    )
    assert spouse_edge.source.record_id == "gramps:Person:H1"


async def test_ingest_families_maps_parents_and_children(ingest):
    service, transport = ingest
    res = await ingest_families(
        [
            {
                "handle": "F1",
                "gramps_id": "F0007",
                "type": {"string": "Married"},
                "father_handle": "HF",
                "mother_handle": "HM",
                "child_ref_list": [{"ref": "HC1"}, {"ref": "HC2"}],
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 4}
    node = transport.requests[0].records[0]
    assert node.record_id == "gramps:Family:F1"
    assert node.payload["familyRelType"] == "Married"
    rels = transport.requests[0].relationships
    father_edge = next(r for r in rels if r.target.record_id == "gramps:Person:HF")
    assert father_edge.source.record_id == "gramps:Family:F1"
    mother_edge = next(r for r in rels if r.target.record_id == "gramps:Person:HM")
    assert mother_edge.source.record_id == "gramps:Family:F1"
    children = [
        r
        for r in rels
        if r.target.record_id in ("gramps:Person:HC1", "gramps:Person:HC2")
    ]
    assert len(children) == 2


async def test_ingest_events_maps_type_date_and_place(ingest):
    service, transport = ingest
    res = await ingest_events(
        [
            {
                "handle": "E1",
                "gramps_id": "E0011",
                "type": "Birth",
                "date": {"text": "1900-01-01"},
                "description": "born",
                "place": "PL1",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    node = transport.requests[0].records[0]
    assert node.record_id == "gramps:Event:E1"
    assert node.payload["eventType"] == "Birth"
    assert node.payload["eventDate"] == "1900-01-01"
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "gramps:Event:E1"
    assert rel.target.record_id == "gramps:Place:PL1"


async def test_ingest_noops_without_engine():
    # No injected ingest + no reachable engine -> clean no-op (best-effort surface).
    assert await ingest_entities([{"id": "a", "node_type": "Person"}]) is None


async def test_ingest_rejects_retired_structural_alias_as_noop(ingest):
    # gramps_mcp's tool surface is best-effort (never raises): a malformed record
    # (the retired ``type`` alias instead of canonical ``node_type``) is reported
    # back as a clean no-op rather than propagating IngestError.
    service, transport = ingest
    assert await ingest_entities([{"id": "a", "type": "Person"}], ingest=service) is None
    assert transport.requests == []


async def test_ingest_empty_is_noop(ingest):
    service, _transport = ingest
    assert await ingest_entities([], ingest=service) is None
    assert await ingest_people([], ingest=service) is None
    assert await ingest_families([], ingest=service) is None
    assert await ingest_events([], ingest=service) is None
