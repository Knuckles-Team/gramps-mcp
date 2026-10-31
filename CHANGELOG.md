# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-27

### Added
- Add the packaged Gramps development skill and spec-delivery Pages dashboard.

## [2.3.4] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [2.3.3] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

## [Unreleased]

### Changed

- Adopted Agent Utilities 1.27.1 current MCP, AgentConfig, TLS-profile, agent-runtime,
  and mandatory full epistemic-graph contracts.
- Regenerated all 147 OpenAPI operations with authority-neutral paths, current action
  resolution, and blocking-call isolation.
- Consolidated three overlapping skills into `gramps-genealogy-operations` with
  living-person privacy, evidence, and write-safety guidance.
- Reworked README, MkDocs, runtime examples, and container deployment around
  reference-only portable configuration.

### Security

- Enforced absolute HTTPS, fixed request authority, encoded path parameters, disabled
  redirects, bounded retries/pagination/responses, sanitized authentication errors, and
  AgentConfig-resolved TLS trust without a boolean bypass.
- Removed environment-specific identities, endpoints, image ownership, model settings,
  filesystem paths, and checked-in credential placeholders.
- Container builds now install the checked-out source, run as an unprivileged user,
  and replace the retired curl-to-shell debug image with the single reviewed build.
- Removed the direct fail-open genealogy/media graph writers; provider presets remain
  inactive inputs for centrally compiled and approved signed GraphOS synchronization.

## [0.1.0] - 2026-06-22

### Added
- Initial release.
- Modular subfolders for API wrappers (`api/`) and action-routed MCP tools (`mcp/`).
- Material-theme mkdocs documentation site (7 standard pages).
- Full pre-commit quality gate and flat `tests/` structure.
