"""Native knowledge-graph ingestion tools for Gramps (Wire-First surface).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists genealogy records via the real
Gramps client and pushes them natively into the ONE epistemic-graph engine — people,
families and events as typed ``:Person``/``:Family``/``:Event`` nodes (+ kinship links),
and media files as content-addressed ``:MediaAsset`` blobs. Best-effort: every tool
returns ``{"ingested": None}`` when no engine is reachable, so it is safe to expose
alongside the read/write tool surface.
"""

from __future__ import annotations

import json as _json
from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from gramps_mcp.auth import get_client


def _records(resp: Any) -> list[dict[str, Any]]:
    """Unwrap a Gramps ``Response`` into a list of plain record dicts."""
    data = getattr(resp, "data", resp)
    records = data if isinstance(data, list) else [data]
    out: list[dict[str, Any]] = []
    for r in records:
        if r is None:
            continue
        out.append(r.model_dump() if hasattr(r, "model_dump") else r)
    return out


def register_kg_tools(mcp: FastMCP):
    @mcp.tool(tags={"kg"})
    async def gramps_ingest_people(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_people query filters (e.g. gramps_id, page).",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest Gramps people into epistemic-graph as typed :Person nodes.

        Lists people via the Gramps API and pushes them (with :spouseInFamily /
        :childInFamily / :participatedInEvent / :hasMedia links) into the KG.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from gramps_mcp.kg_ingest import ingest_people

        kwargs = _json.loads(params_json) if params_json else {}
        people = _records(client.get_people(**kwargs))
        result = ingest_people(people)
        return {"listed": len(people), "ingested": result}

    @mcp.tool(tags={"kg"})
    async def gramps_ingest_families(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_families query filters.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest Gramps families into epistemic-graph as typed :Family nodes.

        Pushes each family with its :hasFather / :hasMother / :hasChild links.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from gramps_mcp.kg_ingest import ingest_families

        kwargs = _json.loads(params_json) if params_json else {}
        families = _records(client.get_families(**kwargs))
        result = ingest_families(families)
        return {"listed": len(families), "ingested": result}

    @mcp.tool(tags={"kg"})
    async def gramps_ingest_events(
        params_json: str = Field(
            default="{}",
            description="JSON string of get_events query filters.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest Gramps events into epistemic-graph as typed :Event nodes (+ :occurredAtPlace).

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from gramps_mcp.kg_ingest import ingest_events

        kwargs = _json.loads(params_json) if params_json else {}
        events = _records(client.get_events(**kwargs))
        result = ingest_events(events)
        return {"listed": len(events), "ingested": result}

    @mcp.tool(tags={"kg"})
    async def gramps_ingest_media(
        handle: str = Field(
            description="Handle of the Gramps media object whose file bytes to ingest."
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest one Gramps media file's raw bytes as a :MediaAsset blob.

        Reads the media object's metadata + its file bytes and stores them as a
        content-addressed blob in the knowledge graph. CONCEPT:AU-KG.ingest.list-durable-media.
        """
        from gramps_mcp.kg_media import ingest_media_blob

        media_records = _records(client.get_media_object(handle=handle))
        media = media_records[0] if media_records else {}
        file_resp = client.get_media_file(handle=handle)
        raw = getattr(file_resp, "response", None)
        data = getattr(raw, "content", None)
        result = ingest_media_blob(data, media=media)
        return {"handle": handle, "ingested": result}

    return None
