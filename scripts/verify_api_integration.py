#!/usr/bin/env python3
"""Verify exact generated API, manifest, and condensed MCP action parity."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _public_api_methods(root: Path) -> set[str]:
    methods: set[str] = set()
    api_dir = root / "gramps_mcp" / "api"
    for path in sorted(api_dir.glob("api_client_*.py")):
        if path.name == "api_client_base.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for item in node.body:
                if isinstance(
                    item, (ast.FunctionDef, ast.AsyncFunctionDef)
                ) and not item.name.startswith("_"):
                    methods.add(item.name)
    return methods


def _manifest_values(root: Path, key: str) -> set[str]:
    path = root / "gramps_mcp" / "api" / "_operation_manifest.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
    for node in tree.body:
        if not isinstance(node, ast.AnnAssign) or not isinstance(node.target, ast.Name):
            continue
        if node.target.id == "OPERATIONS" and node.value is not None:
            operations = ast.literal_eval(node.value)
            return {
                str(operation[key])
                for operation in operations
                if isinstance(operation, dict) and key in operation
            }
    return set()


def _condensed_actions(root: Path) -> set[str]:
    actions: set[str] = set()
    mcp_dir = root / "gramps_mcp" / "mcp"
    for path in sorted(mcp_dir.glob("mcp_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not (
                isinstance(node.func, ast.Name) and node.func.id == "resolve_action"
            ):
                continue
            if len(node.args) < 2 or not isinstance(
                node.args[1], (ast.Set, ast.List, ast.Tuple)
            ):
                continue
            for element in node.args[1].elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    actions.add(element.value)
    return actions


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    methods = _public_api_methods(root)
    manifest_methods = _manifest_values(root, "method")
    manifest_actions = _manifest_values(root, "action")
    actions = _condensed_actions(root)

    failures: list[str] = []
    comparisons = {
        "API methods missing from manifest": methods - manifest_methods,
        "Unknown manifest methods": manifest_methods - methods,
        "Manifest actions missing from MCP": manifest_actions - actions,
        "Unknown MCP actions": actions - manifest_actions,
    }
    for label, values in comparisons.items():
        if values:
            failures.append(f"{label}: {', '.join(sorted(values))}")

    print("Gramps API-to-MCP parity")
    print(f"API methods: {len(methods)}")
    print(f"Manifest actions: {len(manifest_actions)}")
    print(f"Condensed actions: {len(actions)}")
    if failures or not methods:
        for failure in failures:
            print(failure)
        return 1
    print("Coverage: 100.0%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
