import ast
import json
from pathlib import Path

import pytest
import tomllib

import gramps_mcp
from gramps_mcp.mcp_server import get_mcp_instance

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.concept("GM-OS.identity.grmp")
def test_package_import_has_an_explicit_client_only_surface():
    """Importing the package does not probe optional server runtimes."""
    assert gramps_mcp.__all__ == ["Api", "GrampsApiBase"]
    assert not hasattr(gramps_mcp, "get_mcp_instance")
    assert not hasattr(gramps_mcp, "_MCP_AVAILABLE")
    assert not hasattr(gramps_mcp, "_AGENT_AVAILABLE")


@pytest.mark.concept("GM-OS.identity.grmp")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with registered tool domains."""
    monkeypatch.setattr("sys.argv", ["gramps-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None


@pytest.mark.concept("GM-OS.identity.grmp")
def test_provider_has_one_current_skill():
    """The provider exposes one comprehensive skill with UI metadata."""
    skills = sorted((ROOT / "gramps_mcp" / "skills").glob("*/SKILL.md"))
    assert [path.parent.name for path in skills] == ["gramps-genealogy-operations"]
    assert (skills[0].parent / "agents" / "openai.yaml").is_file()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_provider_owns_complete_neutral_source_bundle():
    """Release evidence is complete and never claims external-live validation."""
    connectors = ROOT / "gramps_mcp" / "connectors"
    presets = json.loads(
        (connectors / "mcp_source_presets.json").read_text(encoding="utf-8")
    )
    assert {key for key in presets if not key.startswith("_")} == {
        "gramps-events",
        "gramps-families",
        "gramps-people",
    }
    fingerprints = json.loads(
        (connectors / "tool_schema_fingerprints.json").read_text(encoding="utf-8")
    )
    assert set(fingerprints["tools"]) == {
        "gramps_events",
        "gramps_families",
        "gramps_people",
    }

    ontology = ROOT / "gramps_mcp" / "ontology"
    certification = json.loads(
        (ontology / "certification.json").read_text(encoding="utf-8")
    )
    assert certification["connector"] == "gramps-mcp"
    assert certification["mode"] == "offline-source"
    assert certification["status"] == "source-validated"
    assert certification["live_certified"] is False
    for relative in (
        "connector_manifest.yml",
        "gramps_mcp/ontology/shapes/connector.shacl.ttl",
        "gramps_mcp/ontology/mappings/source.yaml",
        "gramps_mcp/ontology/fixtures/records.json",
        "gramps_mcp/ontology/migrations/manifest.json",
    ):
        assert relative in certification["artifacts"]
        assert (ROOT / relative).is_file()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_provider_entry_points_prove_package_ownership():
    """Every provider leg resolves to a data package in the owning wheel."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    entry_points = project["project"]["entry-points"]
    assert entry_points["agent_utilities.skill_providers"] == {
        "gramps-mcp": "gramps_mcp.skills"
    }
    assert entry_points["agent_utilities.ontology_providers"] == {
        "gramps-mcp": "gramps_mcp.ontology"
    }
    assert entry_points["agent_utilities.source_connector_providers"] == {
        "gramps-mcp": "gramps_mcp.connectors"
    }
    assert entry_points["agent_utilities.prompt_providers"] == {
        "gramps-mcp": "gramps_mcp.prompts"
    }


@pytest.mark.concept("GM-OS.identity.grmp")
def test_direct_graph_write_surface_is_absent():
    """Genealogy records can enter the graph only through central source sync."""
    package = ROOT / "gramps_mcp"
    assert not (package / "kg_ingest.py").exists()
    assert not (package / "kg_media.py").exists()
    assert not (package / "mcp" / "mcp_kg.py").exists()
    assert not (package / "api_client.py").exists()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_generated_operation_manifest_contains_relative_paths_only():
    """A source specification cannot bake its authority into generated clients."""
    manifest = ROOT / "gramps_mcp" / "api" / "_operation_manifest.py"
    tree = ast.parse(manifest.read_text(encoding="utf-8"))
    operations = None
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "OPERATIONS":
                operations = ast.literal_eval(node.value)
                break
    assert operations
    assert all(str(operation["path"]).startswith("/api/") for operation in operations)
    assert all("://" not in str(operation["path"]) for operation in operations)


@pytest.mark.concept("GM-OS.identity.grmp")
def test_dependency_contract_uses_current_runtime():
    """Provider metadata requires the current Agent Utilities contract."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["dependencies"] == ["agent-utilities>=1.27.1,<2.0.0"]
    assert project["project"]["optional-dependencies"]["agent"] == [
        "agent-utilities[agent-runtime,logfire]>=1.27.1,<2.0.0"
    ]
