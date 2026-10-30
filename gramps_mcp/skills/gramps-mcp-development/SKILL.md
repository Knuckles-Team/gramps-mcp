---
name: gramps-mcp-development
domain: development
skill_type: skill
description: >-
  Develop, test, gate, and release the gramps-mcp connector. Use this skill when
  changing Gramps API mappings, governed MCP tools, genealogy ingestion, packaged
  connector content, documentation, or repository gates.
license: MIT
tags: [gramps, genealogy, development, connector, mcp, test, gates]
tier: repository
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# gramps-mcp development

This repository owns the Gramps Web API clients, typed genealogy models,
action-routed MCP tools, source declarations, knowledge-graph ingestion mappings,
and packaged connector content. Shared connector contracts, transports, TLS
profiles, and credential helpers belong to `scion-sdk`; admission,
serving, and durable graph state belong to their owning repositories. Read
`AGENTS.md` before changing code and keep credentials, private endpoints,
personal records, and customer data out of source, logs, fixtures, and skill
content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the owning
spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding requirement text. `PIPE-CONNSPEC-R126.4` is a
  central pipelines criterion; do not invent a local status row for it.
- Reuse the one `Connector` in `gramps_mcp/__init__.py`, the API clients under
  `gramps_mcp/api/`, the action-routed tools under `gramps_mcp/mcp/`, and the
  existing ingestion boundaries in `gramps_mcp/kg_ingest.py` and
  `gramps_mcp/kg_media.py`. Do not create a second API, MCP, authentication,
  transport, or graph-write plane.
- Preserve the `GRAMPS_URL`, token/login settings, and SDK TLS resolution in
  `gramps_mcp/auth.py`. Never hardcode a secret, endpoint, personal record, or
  TLS-verification bypass.
- Keep the source declarations in `gramps_mcp/connector_sources.py`, typed
  models, ontology mappings, and action registrations aligned with the SDK
  dynamic surface. Keep tenant, tree, and installation data neutral.
- Every delivered requirement needs a bound focused test. Generated
  `specs/*/status.json` files come from the shared hooks; never hand-edit them.
- Keep `gramps_mcp/skills/`, ontology, prompts, `mcp_config.json`, and source
  declarations coherent with the existing package-data and `gramps-mcp` entry
  point. One logical change per commit, using `Spec: none (<reason>)` for a
  central criterion with no local requirements row.

## Setup and gates

Use the locked environment, then run the shared gates:

```bash
uv sync --locked
uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

For focused feedback, run the smallest affected test with the locked
environment:

```bash
uv run --locked --extra test pytest -q tests/test_pages_workflow.py
```

The canonical `.pre-commit-config.yaml` delegates connector-standard, secrets,
spec, tests-fast, and dependency-readiness checks to `Knuckles-Team/pipelines`
at `rev: main`. Do not copy those hooks locally or bypass a failing check.

## Connector-specific checks

- Keep Gramps API methods behind the existing client modules and action-routed
  MCP registration. Validate response models and translate provider failures
  through the existing SDK and client boundaries.
- Preserve bearer-token or login handling and SDK TLS resolution. Mock Gramps
  HTTP responses in local tests; never call a live instance or use live
  credentials in a gate.
- Keep `gramps_mcp/skills/`, `gramps_mcp/ontology/`, `gramps_mcp/connectors/`,
  prompts, and `mcp_config.json` in package data. Keep source declarations and
  ontology mappings explicit and installation-neutral.
- Documentation is published by `.github/workflows/pages.yml`, which calls
  `pages_pipeline.yml@main`. The Python release and rendered connector image
  are called by `.github/workflows/pipeline.yml`; do not add a second publisher
  or commit generated Docker artifacts.

## Packaging and publication

`pyproject.toml` declares the `gramps-mcp` entry point and packages `skills/**`,
prompts, ontology, connector content, and `mcp_config.json`. For a packaged
content release, keep the project version, `CHANGELOG.md`, and the editable
`gramps-mcp` entry in `uv.lock` coherent, then inspect `uv build` output for
`gramps_mcp/skills/gramps-mcp-development/SKILL.md`.

The canonical release caller is `.github/workflows/pipeline.yml`: it publishes
the Python connector with `python_pipeline.yml@main`, then builds the rendered
connector container with `container_pipeline.yml@main` and
`render_connector: true`. Do not claim package, container, or Pages publication
from a local build; require exact-source hosted evidence and the public
artifact.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate. Do
not use `git stash`, `git add -A`, or `git add .`; preserve unrelated working
tree changes. Keep runtime, ontology, source status, and generated artifacts
outside a bounded skill slice unless the owning requirement explicitly requires
them.
