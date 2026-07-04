"""Native epistemic-graph ingestion for Gramps genealogy records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
the blob ingestion in :mod:`gramps_mcp.kg_media`: the connector natively pushes its
genealogy data into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:Person``, ``:Family``, ``:Event``, ``:Place``, …) plus kinship/participation links.

Ingestion rides the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` when it is available; because
that primitive is not yet in every installed ``agent_utilities``, the import is GUARDED
and a self-contained txn fallback (the same fast ``GraphComputeEngine()._client`` + txn
dance) is used otherwise. Either way everything is dependency-/engine-guarded: with no KG
stack or no reachable engine every entry point **no-ops** (returns ``None``), so the
connector runs with zero KG infrastructure. Node ids follow ``gramps:<class>:<handle>``
and each ``type`` matches a class the package's ``gramps.ttl`` federates.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("gramps_mcp.kg")

_SOURCE = "gramps-mcp"
_DOMAIN = "gramps"

_GENDER = {0: "female", 1: "male", 2: "unknown"}


# --------------------------------------------------------------------------- #
# write path — delegate to the shared primitive, else a self-contained fallback
# --------------------------------------------------------------------------- #
def _native() -> Any | None:
    """Return the shared native_ingest module, or ``None`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest
    except Exception as e:  # noqa: BLE001 — primitive not installed yet
        logger.debug("native_ingest primitive unavailable: %s", e)
        return None


def _fallback_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or "__commons__")
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any | None,
    graph: str | None,
) -> dict[str, int] | None:
    """Self-contained txn write when the shared primitive is not importable."""
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    graph = graph or "__commons__"
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)
    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph. Never raises.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / empty / failure).
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    if not entities:
        return None
    if client is None:
        native = _native()
        if native is not None:
            return native.ingest_entities(
                entities, relationships, source=source, domain=domain
            )
    return _fallback_write(entities, relationships, client=client, graph=graph)


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records (e.g. genealogy notes) as ``:Document`` nodes. Never raises."""
    if not documents:
        return None
    if client is None:
        native = _native()
        if native is not None:
            return native.ingest_documents(documents, source=source, domain=domain)
    nodes: list[dict[str, Any]] = []
    for doc in documents:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        nodes.append(node)
    return _fallback_write(nodes, None, client=client, graph=graph)


# --------------------------------------------------------------------------- #
# mappers — Gramps records → typed entity/relationship dicts
# --------------------------------------------------------------------------- #
def _display_name(person: dict[str, Any]) -> str | None:
    name = person.get("primary_name") or {}
    if not isinstance(name, dict):
        return None
    first = name.get("first_name") or ""
    surnames = name.get("surname_list") or []
    surname = ""
    if surnames and isinstance(surnames[0], dict):
        surname = surnames[0].get("surname") or ""
    full = f"{first} {surname}".strip()
    return full or None


def _refs(record: dict[str, Any], key: str) -> list[str]:
    """Extract handles from a Gramps ref list (``[{"ref": handle}, …]`` or ``[handle]``)."""
    out: list[str] = []
    for item in record.get(key) or []:
        if isinstance(item, dict):
            ref = item.get("ref")
        else:
            ref = item
        if ref:
            out.append(ref)
    return out


def ingest_people(
    people: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Gramps person records → ``:Person`` nodes + family/event links, then ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for person in people or []:
        handle = person.get("handle")
        if not handle:
            continue
        pid = f"gramps:Person:{handle}"
        gender = person.get("gender")
        entities.append(
            {
                "id": pid,
                "type": "Person",
                "name": _display_name(person),
                "grampsId": person.get("gramps_id"),
                "handle": handle,
                "gender": _GENDER.get(gender) if isinstance(gender, int) else gender,
                "externalToolId": handle,
            }
        )
        for fam in _refs(person, "family_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:Family:{fam}",
                    "type": "spouseInFamily",
                }
            )
        for fam in _refs(person, "parent_family_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:Family:{fam}",
                    "type": "childInFamily",
                }
            )
        for ev in _refs(person, "event_ref_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:Event:{ev}",
                    "type": "participatedInEvent",
                }
            )
        for md in _refs(person, "media_list"):
            relationships.append(
                {"source": pid, "target": f"gramps:MediaAsset:{md}", "type": "hasMedia"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_families(
    families: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Gramps family records → ``:Family`` nodes + father/mother/child links."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for fam in families or []:
        handle = fam.get("handle")
        if not handle:
            continue
        fid = f"gramps:Family:{handle}"
        rel_type = fam.get("type")
        if isinstance(rel_type, dict):
            rel_type = rel_type.get("string") or rel_type.get("value")
        entities.append(
            {
                "id": fid,
                "type": "Family",
                "grampsId": fam.get("gramps_id"),
                "handle": handle,
                "familyRelType": rel_type,
                "externalToolId": handle,
            }
        )
        if fam.get("father_handle"):
            relationships.append(
                {
                    "source": fid,
                    "target": f"gramps:Person:{fam['father_handle']}",
                    "type": "hasFather",
                }
            )
        if fam.get("mother_handle"):
            relationships.append(
                {
                    "source": fid,
                    "target": f"gramps:Person:{fam['mother_handle']}",
                    "type": "hasMother",
                }
            )
        for child in _refs(fam, "child_ref_list"):
            relationships.append(
                {
                    "source": fid,
                    "target": f"gramps:Person:{child}",
                    "type": "hasChild",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_events(
    events: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Gramps event records → ``:Event`` nodes + place links, then ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for ev in events or []:
        handle = ev.get("handle")
        if not handle:
            continue
        eid = f"gramps:Event:{handle}"
        ev_type = ev.get("type")
        if isinstance(ev_type, dict):
            ev_type = ev_type.get("string") or ev_type.get("value")
        date = ev.get("date")
        if isinstance(date, dict):
            date = date.get("text") or date.get("dateval") or date.get("sortval")
        entities.append(
            {
                "id": eid,
                "type": "Event",
                "grampsId": ev.get("gramps_id"),
                "handle": handle,
                "eventType": ev_type,
                "eventDate": str(date) if date is not None else None,
                "description": ev.get("description"),
                "externalToolId": handle,
            }
        )
        place = ev.get("place")
        if place:
            relationships.append(
                {
                    "source": eid,
                    "target": f"gramps:Place:{place}",
                    "type": "occurredAtPlace",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)
