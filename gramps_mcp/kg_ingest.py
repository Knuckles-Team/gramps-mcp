"""Native epistemic-graph ingestion for Gramps genealogy records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
the blob ingestion in :mod:`gramps_mcp.kg_media`: the connector natively pushes its
genealogy data into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:Person``, ``:Family``, ``:Event``, ``:Place``, …) plus kinship/participation links,
through the required ``agent_utilities.knowledge_graph.memory.native_ingest`` authority
— the one connector write path; there is no self-contained fallback transaction here.

The MCP tool surface (``gramps_mcp.mcp.mcp_kg``) exposes these as best-effort tools that
must never raise on an unreachable/misconfigured KG stack, so ``ingest_entities`` /
``ingest_documents`` stay **best-effort**: they return ``None`` (never raise) for empty
input or when the shared primitive reports :class:`NativeIngestError` (no reachable
engine, or a malformed record). Node ids follow ``gramps:<class>:<handle>`` and each
``node_type`` matches a class the package's ``gramps.ttl`` federates.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    NativeIngestError,
    ingest_documents as _native_ingest_documents,
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("gramps_mcp.kg")

_SOURCE = "gramps-mcp"
_DOMAIN = "gramps"

_GENDER = {0: "female", 1: "male", 2: "unknown"}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph. Best-effort, never raises.

    ``entities``: ``[{"id":..., "node_type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "relationship":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (empty input / no reachable engine /
    malformed record). ``client``/``graph`` may be injected (tests); otherwise the
    process-owned governed authority is resolved on demand.
    """
    if not entities:
        return None
    try:
        return _native_ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records (e.g. genealogy notes) as ``:Document`` nodes. Best-effort."""
    if not documents:
        return None
    try:
        return _native_ingest_documents(
            documents, source=source, domain=domain, client=client, graph=graph
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


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
                "node_type": "Person",
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
                    "relationship": "spouseInFamily",
                }
            )
        for fam in _refs(person, "parent_family_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:Family:{fam}",
                    "relationship": "childInFamily",
                }
            )
        for ev in _refs(person, "event_ref_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:Event:{ev}",
                    "relationship": "participatedInEvent",
                }
            )
        for md in _refs(person, "media_list"):
            relationships.append(
                {
                    "source": pid,
                    "target": f"gramps:MediaAsset:{md}",
                    "relationship": "hasMedia",
                }
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
                "node_type": "Family",
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
                    "relationship": "hasFather",
                }
            )
        if fam.get("mother_handle"):
            relationships.append(
                {
                    "source": fid,
                    "target": f"gramps:Person:{fam['mother_handle']}",
                    "relationship": "hasMother",
                }
            )
        for child in _refs(fam, "child_ref_list"):
            relationships.append(
                {
                    "source": fid,
                    "target": f"gramps:Person:{child}",
                    "relationship": "hasChild",
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
                "node_type": "Event",
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
                    "relationship": "occurredAtPlace",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)
