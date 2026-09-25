"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_people`` / ``ingest_families`` /
``ingest_events`` seam with a fake ChangeEnvelope-capable engine client (no engine
required), asserting the committed nodes/edges and the Gramps record -> typed-node
mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake client mirrors agent-utilities' own sanctioned test double
(``agent-utilities/tests/knowledge_graph/test_native_ingest.py``) — the ``txn``-only
fake is retired; ``native_ingest`` now hard-requires an injected client exposing
``.changes``/``.nodes``/``.rdf``/``.supports()``. Unlike most fleet connectors,
``gramps_mcp.kg_ingest`` is a **best-effort** surface (its MCP tools must never raise
when the KG stack is down), so it converts ``NativeIngestError`` into ``None`` rather
than propagating it — those semantics are exercised explicitly below.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.security.actor_identity import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from gramps_mcp.kg_ingest import (
    ingest_entities,
    ingest_events,
    ingest_families,
    ingest_people,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"

    @staticmethod
    def shacl_validate_committed(_data_graph: str) -> Any:
        """EG's committed-GraphSchema SHACL authority (agent-utilities EH-385)."""
        from epistemic_graph.generated.rdf_report import ShaclValidationReport

        digest = "sha256:" + "0" * 64
        return ShaclValidationReport(
            conforms=True, results=[], composed_digest=digest, schema_digests=[digest]
        )


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Person", "name": "p"},
            {"id": "b", "node_type": "Family"},
        ],
        [{"source": "a", "target": "b", "relationship": "spouseInFamily"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "gramps-mcp"
    assert c.nodes.values["a"]["domain"] == "gramps"
    assert c.changes.edges == [("a", "b", {"relationship": "spouseInFamily"})]


def test_ingest_people_maps_person_and_links():
    c = _FakeClient()
    res = ingest_people(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 4}
    node = c.nodes.values["gramps:Person:H1"]
    assert node["node_type"] == "Person"
    assert node["name"] == "John Doe"
    assert node["gender"] == "male"
    assert node["grampsId"] == "I0042"
    assert node["externalToolId"] == "H1"
    edge_types = {e[2]["relationship"] for e in c.changes.edges}
    assert edge_types == {
        "spouseInFamily",
        "childInFamily",
        "participatedInEvent",
        "hasMedia",
    }
    assert (
        "gramps:Person:H1",
        "gramps:Family:F1",
        {"relationship": "spouseInFamily"},
    ) in c.changes.edges


def test_ingest_families_maps_parents_and_children():
    c = _FakeClient()
    res = ingest_families(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 4}
    node = c.nodes.values["gramps:Family:F1"]
    assert node["node_type"] == "Family"
    assert node["familyRelType"] == "Married"
    assert (
        "gramps:Family:F1",
        "gramps:Person:HF",
        {"relationship": "hasFather"},
    ) in c.changes.edges
    assert (
        "gramps:Family:F1",
        "gramps:Person:HM",
        {"relationship": "hasMother"},
    ) in c.changes.edges
    children = [e for e in c.changes.edges if e[2]["relationship"] == "hasChild"]
    assert len(children) == 2


def test_ingest_events_maps_type_date_and_place():
    c = _FakeClient()
    res = ingest_events(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 1}
    node = c.nodes.values["gramps:Event:E1"]
    assert node["node_type"] == "Event"
    assert node["eventType"] == "Birth"
    assert node["eventDate"] == "1900-01-01"
    assert c.changes.edges == [
        ("gramps:Event:E1", "gramps:Place:PL1", {"relationship": "occurredAtPlace"})
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op (best-effort surface).
    assert ingest_entities([{"id": "a", "node_type": "Person"}]) is None


def test_ingest_rejects_retired_structural_alias_as_noop():
    # gramps_mcp's tool surface is best-effort (never raises): a malformed record
    # (the retired ``type`` alias instead of canonical ``node_type``) is reported
    # back as a clean no-op rather than propagating NativeIngestError.
    c = _FakeClient()
    assert ingest_entities([{"id": "a", "type": "Person"}], client=c) is None
    assert c.changes.applied == []


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_people([], client=_FakeClient()) is None
    assert ingest_families([], client=_FakeClient()) is None
    assert ingest_events([], client=_FakeClient()) is None
