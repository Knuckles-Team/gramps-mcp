---
name: gramps-genealogy-operations
skill_type: skill
description: >-
  Research and administer an authorized Gramps family-history system through gramps-mcp: people, families, events, places, sources, media, DNA, timelines, imports, exports, trees and users. Use for evidence-based lookup, kinship resolution, record management, approved mutations, or requesting governed Arbora sync. Full scope in body.
---

# Gramps Genealogy Operations

Scope: Research and administer an authorized Gramps family-history system through gramps-mcp, including people, families, events, places, relationships, sources, citations, notes, media, DNA, timelines, imports, exports, trees, users, and supporting configuration. Use for evidence-based genealogy lookup, kinship resolution, media or record management, carefully approved mutations, or requesting centrally governed Arbora synchronization of Gramps records.

Use the `gramps-mcp` server as the typed boundary to an operator-selected Gramps Web
API. Treat genealogy records as sensitive personal data, especially records about
living people, DNA, notes, media, contact details, user accounts, and authentication.

## Steps

1. Establish the authorized tree and the minimum record scope, and call `gramps_get_metadata` to confirm the connection.
   Verify the response names the expected tree.
2. Find the target with `gramps_get_search` or `gramps_get_people` using a `gramps_id` or narrow query.
   Verify exactly one `handle` is selected.
3. Read the record and its linked events, sources and citations with `gramps_get_person` (`handle`) and the matching typed reads.
   Verify conclusions are backed by a citation and flag any that are not.
4. Check living or sensitive status with `gramps_get_living` (`handle`) before returning personal details.
   Verify living persons are withheld or the operator approved release.
5. For a mutation, state the objects and effect, get explicit approval, and call the typed write tool such as `gramps_put_person`.
   Verify by reading the record back with `gramps_get_person`.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| HTTP 401 or 403 from any tool | `GRAMPS_TOKEN` or `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` missing or expired, or the account role is too low for a write | Set valid credentials for the `gramps-mcp` server, then call `gramps_get_metadata` to confirm the session works; ask the operator for an editor-role account before any write |
| Not-found error for a handle | A `gramps_id` such as `I0042` was passed where the opaque `handle` is required, or the handle is from another tree | Resolve the record with the list tool and its `gramps_id` filter, then pass the `handle` it returns |
| Ambiguous or empty search | Name-only query matches several people or none | Narrow with `gramps_id` or `rules` filters via `gramps_get_people`, and ask the operator to pick the handle; never assume identity from a name |
| Destructive tool refused | `confirm=true` missing or operator approval absent | Describe the exact objects to the operator, obtain approval, and pass `confirm=true` |

## Invoke the tools

Call the typed tool for the operation (`gramps_get_person`, `gramps_post_tags`, ...); each
Gramps Web API operation is its own tool and takes real arguments. Use exact tool names
exposed by the server; do not invent a raw HTTP call or infer a record from a display name.

Common domains (tool-name stems):

- Research: `gramps_people`, `gramps_families`, `gramps_events`, `gramps_places`,
  `gramps_relations`, `gramps_timeline`, `gramps_search`, `gramps_living`.
- Evidence: `gramps_sources`, `gramps_citations`, `gramps_repositories`,
  `gramps_notes`, `gramps_facts`, `gramps_tags`, `gramps_media`.
- Data movement: `gramps_importers`, `gramps_exporters`, `gramps_reports`,
  `gramps_transactions`, `gramps_tasks`.
- Administration: `gramps_trees`, `gramps_users`, `gramps_config`, `gramps_oidc`,
  `gramps_token`, `gramps_metadata`, `gramps_types`, `gramps_filters`,
  `gramps_name_formats`, `gramps_name_groups`, `gramps_bookmarks`,
  `gramps_translations`, `gramps_holidays`, `gramps_chat`, `gramps_dna`.

## Follow the core workflow

1. Establish the authorized tree, purpose, and minimum record scope. Ask for a stable
   `handle`, `gramps_id`, or narrow search criteria when the target is ambiguous.
2. Determine whether the subject may be living or otherwise sensitive. Minimize fields,
   page size, media, and DNA access; do not broaden the query for convenience.
3. Read before writing. Resolve reference-list handles with typed reads and distinguish
   the opaque stable `handle` from the human-facing `gramps_id`.
4. Corroborate conclusions with event, source, citation, and repository records. Mark
   conflicts or inference explicitly; do not turn an unsourced tree assertion into fact.
5. For a mutation, state the exact objects and expected effect. Obtain explicit approval
   before merges, imports, deletes, transaction undo, tree repair or migration, account
   changes, owner creation, password/token operations, or bulk media operations.
6. Execute the smallest approved operation, then read the affected record back. Report
   stable identifiers, status, and evidence without reproducing unrelated private fields.

## Apply genealogy safety

- Never assume parentage, partnership, identity, gender, or living status from a name.
- Never merge merely because names or dates are similar. Compare identifiers, relatives,
  events, places, and citations first.
- Treat DNA matches as highly sensitive. Return only the minimum result authorized for
  the stated purpose and avoid health, ethnicity, or identity conclusions not present in
  the record.
- Do not place media bytes, exports, reports, credentials, endpoint values, or local
  filesystem paths in prompts, logs, telemetry, or durable scratch files.
- Do not expose token responses, password-reset artifacts, OIDC callbacks, user emails,
  or exception bodies. Prefer delegated identity when the deployment supports it.
- Keep pagination bounded. For bulk work, process explicit pages and report counts rather
  than emitting an entire tree into the conversation.

## Use governed graph synchronization

This provider has no direct graph-write or raw-media-ingestion tool. If Gramps records
must enter medulla, request Arbora source synchronization using a centrally
compiled and operator-approved signed capability bundle. Require exact live tool-schema
pins plus tenant, ACL, classification, consent, retention, provenance, redaction, and
deletion policy. A missing or stale certification must fail closed.

The packaged ontology and source presets describe only the public Gramps model. They are
not authorization to ingest a live tree and contain no instance-specific mapping.

## Respect the runtime boundary

Resolve the endpoint, fixed credentials or delegated identity, and TLS profile through
AgentConfig at runtime. The endpoint must be HTTPS. Never disable peer or hostname
verification, embed credentials in a URL, or persist a resolved secret, certificate
path, endpoint, tenant value, personal identifier, or telemetry destination in code.
