"""Verify the connector's Pages caller and packaged development skill contract."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_CONFIG = ROOT / ".github/spec-dashboard.json"
DEVELOPMENT_SKILL = ROOT / "gramps_mcp/skills/gramps-mcp-development/SKILL.md"


def _events(workflow: dict) -> dict:
    # YAML 1.1 parsers expose the unquoted `on` key as True.
    events = workflow.get("on", workflow.get(True))
    assert isinstance(events, dict)
    return events


@pytest.mark.spec("PIPE-CONNSPEC-R126.3")
def test_pages_caller_enables_dashboard_and_pages_permissions() -> None:
    assert not (ROOT / ".github/workflows/docs.yml").exists()


@pytest.mark.spec("PIPE-CONNSPEC-R126.4")
def test_development_skill_has_rapid_contract_and_package_binding() -> None:
    text = DEVELOPMENT_SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert DEVELOPMENT_SKILL.is_file()
    assert "name: gramps-mcp-development" in frontmatter
    assert "skill_type: skill" in frontmatter
    assert "## Rapid delivery: the 5-minute contract" in text
    for term in (
        "gramps_mcp/__init__.py",
        "gramps_mcp/api/",
        "gramps_mcp/mcp/",
        "gramps_mcp/auth.py",
        "gramps_mcp/connector_sources.py",
        "gramps_mcp/kg_ingest.py",
        "gramps_mcp/kg_media.py",
        "GRAMPS_URL",
        "gramps-mcp",
        "mcp_config.json",
        "skills/**",
        "python_pipeline.yml@main",
        "container_pipeline.yml@main",
        "pages_pipeline.yml@main",
        "render_connector: true",
        "uv run --locked --extra test pytest",
    ):
        assert term in text

    assert "verify=False" not in text
    assert "--no-verify" not in text
    package_data = project["tool"]["setuptools"]["package-data"]["gramps_mcp"]
    assert "skills/**" in package_data
    assert project["project"]["entry-points"]["agent_connector_sdk.connector"] == {
        "gramps-mcp": "gramps_mcp:connector"
    }


def test_pages_dashboard_config_is_canonical() -> None:
    assert json.loads(DASHBOARD_CONFIG.read_text(encoding="utf-8")) == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
