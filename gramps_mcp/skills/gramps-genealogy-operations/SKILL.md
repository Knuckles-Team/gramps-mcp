---
name: gramps-genealogy-operations
description: Research and administer an authorized Gramps family-history system through gramps-mcp, including people, families, events, places, relationships, sources, citations, notes, media, DNA, timelines, imports, exports, trees, users, and supporting configuration. Use for evidence-based genealogy lookup, kinship resolution, media or record management, carefully approved mutations, or requesting centrally governed GraphOS synchronization of Gramps records.
---

# Gramps Genealogy Operations

Use the `gramps-mcp` server as the typed boundary to an operator-selected Gramps Web
API. Treat genealogy records as sensitive personal data, especially records about
living people, DNA, notes, media, contact details, user accounts, and authentication.

## Invoke the tools

Prefer the condensed tool for a domain. Pass its documented `action` and serialize
parameters as a JSON object in `params_json`. Use exact actions exposed by the server;
do not invent a raw HTTP call or infer a record from a display name.

Common domains:

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
must enter epistemic-graph, request GraphOS source synchronization using a centrally
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
