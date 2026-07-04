"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_people`` / ``ingest_families`` /
``ingest_events`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the Gramps record -> typed-node mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from gramps_mcp.kg_ingest import (
    ingest_entities,
    ingest_events,
    ingest_families,
    ingest_people,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [{"id": "a", "type": "Person", "name": "p"}, {"id": "b", "type": "Family"}],
        [{"source": "a", "target": "b", "type": "spouseInFamily"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "gramps-mcp"
    assert c.txn.nodes["a"]["domain"] == "gramps"
    assert c.edges.edges == [("a", "b", {"type": "spouseInFamily"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 4}
    node = c.txn.nodes["gramps:Person:H1"]
    assert node["type"] == "Person"
    assert node["name"] == "John Doe"
    assert node["gender"] == "male"
    assert node["grampsId"] == "I0042"
    assert node["externalToolId"] == "H1"
    edge_types = {e[2]["type"] for e in c.edges.edges}
    assert edge_types == {
        "spouseInFamily",
        "childInFamily",
        "participatedInEvent",
        "hasMedia",
    }
    assert (
        "gramps:Person:H1",
        "gramps:Family:F1",
        {"type": "spouseInFamily"},
    ) in c.edges.edges


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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 4}
    node = c.txn.nodes["gramps:Family:F1"]
    assert node["type"] == "Family"
    assert node["familyRelType"] == "Married"
    assert (
        "gramps:Family:F1",
        "gramps:Person:HF",
        {"type": "hasFather"},
    ) in c.edges.edges
    assert (
        "gramps:Family:F1",
        "gramps:Person:HM",
        {"type": "hasMother"},
    ) in c.edges.edges
    children = [e for e in c.edges.edges if e[2]["type"] == "hasChild"]
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 1}
    node = c.txn.nodes["gramps:Event:E1"]
    assert node["type"] == "Event"
    assert node["eventType"] == "Birth"
    assert node["eventDate"] == "1900-01-01"
    assert c.edges.edges == [
        ("gramps:Event:E1", "gramps:Place:PL1", {"type": "occurredAtPlace"})
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Person"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_people([], client=_FakeClient()) is None
    assert ingest_families([], client=_FakeClient()) is None
    assert ingest_events([], client=_FakeClient()) is None
