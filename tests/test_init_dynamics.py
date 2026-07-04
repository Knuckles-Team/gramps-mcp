import importlib

import pytest


@pytest.mark.concept("GM-OS.identity.grmp")
def test_package_imports():
    """Top-level package exposes its public API. CONCEPT:GM-OS.identity.grmp"""
    module = importlib.import_module("gramps_mcp")
    assert hasattr(module, "__all__")
