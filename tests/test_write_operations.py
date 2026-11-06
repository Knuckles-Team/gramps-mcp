"""Object write operations exist and carry a JSON body (CONN-GRAMPS-MCP-CONNECTOR-CONTENT-R002)."""

import pytest

from gramps_mcp.api import Api
from gramps_mcp.api._operation_manifest import OPERATIONS

OBJECT_TYPES = {
    "people": "person",
    "families": "family",
    "events": "event",
    "places": "place",
    "citations": "citation",
    "sources": "source",
    "repositories": "repository",
    "media_objects": "media_object",
    "notes": "note",
    "tags": "tag",
}
BY_ID = {op["operation_id"]: op for op in OPERATIONS}


@pytest.mark.parametrize("plural,single", OBJECT_TYPES.items())
def test_object_crud_operations_are_served(plural, single):
    assert BY_ID[f"post_{plural}"]["http"] == "POST"
    assert BY_ID[f"put_{single}"]["http"] == "PUT"
    assert BY_ID[f"delete_{single}"]["http"] == "DELETE"
    for name in (f"post_{plural}", f"put_{single}", f"delete_{single}"):
        assert callable(getattr(Api, name))


def test_write_operations_accept_a_body():
    for op in OPERATIONS:
        if op["http"] in {"POST", "PUT"} and op["operation_id"] in {
            "post_objects",
            "post_users",
            "put_user",
            "post_people",
        }:
            assert any(p["name"] == "body" for p in op["params"]), op["operation_id"]
