from pathlib import Path

import pytest

CONCEPTS_DOC = Path(__file__).resolve().parents[1] / "docs" / "concepts.md"


@pytest.mark.concept("GM-OS.identity.grmp")
def test_concepts_doc_exists():
    """Concept registry doc exists. CONCEPT:GM-OS.identity.grmp"""
    assert CONCEPTS_DOC.is_file()


@pytest.mark.concept("GM-OS.identity.grmp")
def test_eco_bridge_present():
    """ECO-4.0 bridge concept is referenced. CONCEPT:GM-OS.identity.grmp"""
    assert "AU-ECO.messaging.native-backend-abstraction" in CONCEPTS_DOC.read_text(encoding="utf-8")


@pytest.mark.concept("GM-OS.identity.grmp")
def test_prefix_registered():
    """Project concept prefix is registered. CONCEPT:GM-OS.identity.grmp"""
    assert "CONCEPT:GRMP-" in CONCEPTS_DOC.read_text(encoding="utf-8")
