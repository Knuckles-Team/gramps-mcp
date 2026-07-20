# Overview

`gramps-mcp` has three layers:

1. Generated domain clients call the configured Gramps Web API through one hardened
   HTTPS base client.
2. Condensed MCP tools route validated actions through the current Agent Utilities
   dispatcher and move blocking HTTP work off the async event loop.
3. The optional A2A server uses the current Agent Utilities agent runtime and the single
   `gramps-genealogy-operations` skill.

## Current runtime contracts

- Agent Utilities 1.27.1 or newer supplies AgentConfig, MCP registration, delegated
  authentication, transport-security profiles, and the mandatory
  `epistemic-graph[full]` base dependency.
- The vendored OpenAPI specification generates 147 operations across 35 domains. The
  generated paths are relative and cannot retain a source-spec authority.
- The configured Gramps origin must be HTTPS. Redirects are not followed, path values
  are encoded, and requests cannot change authority or override TLS policy.
- Fixed credentials and delegated identity are runtime-only. Logs and exceptions omit
  endpoints, subjects, record content, and response bodies.

## Capability ownership

The package owns human-reviewed ontology, source-preset, prompt, and skill inputs plus a
release-generated signed capability bundle with exact local schema fingerprints,
SHACL shapes, neutral fixtures, mappings, migrations, and an offline source attestation.
It does not own deployment endpoints, tenant policy, source records, or external-live
evidence. Missing or stale evidence fails closed.
