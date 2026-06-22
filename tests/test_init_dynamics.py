import importlib

import pytest


@pytest.mark.concept("GRMP-001")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:GRMP-001"""
    module = importlib.import_module("gramps_web_mcp")
    assert hasattr(module, "__all__")
