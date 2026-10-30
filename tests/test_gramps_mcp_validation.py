import ast
import tomllib
from pathlib import Path

import pytest
from scion_sdk.connector import build_server

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.concept("GM-OS.identity.grmp")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with registered tool domains."""
    monkeypatch.setattr("sys.argv", ["gramps-mcp"])
    _, mcp = build_server("gramps_mcp", command_args=[])
    assert mcp is not None


@pytest.mark.concept("GM-OS.identity.grmp")
def test_provider_has_one_current_skill():
    """The provider exposes one comprehensive skill with UI metadata."""
    skills = sorted((ROOT / "gramps_mcp" / "skills").glob("*/SKILL.md"))
    names = [path.parent.name for path in skills]
    assert "gramps-genealogy-operations" in names
    operations = skills[names.index("gramps-genealogy-operations")].parent
    assert (operations / "agents" / "openai.yaml").is_file()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_generated_operation_manifest_contains_relative_paths_only():
    """A source specification cannot bake its authority into generated clients."""
    manifest = ROOT / "gramps_mcp" / "api" / "_operation_manifest.py"
    tree = ast.parse(manifest.read_text(encoding="utf-8"))
    operations = None
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id == "OPERATIONS":
                assert node.value is not None
                operations = ast.literal_eval(node.value)
                break
    assert operations
    assert all(str(operation["path"]).startswith("/api/") for operation in operations)
    assert all("://" not in str(operation["path"]) for operation in operations)


@pytest.mark.concept("GM-OS.identity.grmp")
def test_dependency_contract_uses_current_runtime():
    """Provider metadata requires the current Agent Utilities contract."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert "scion-sdk[mcp]>=0.6.2,<0.7.0" in project["project"]["dependencies"]
    assert "agent" not in project["project"]["optional-dependencies"]
