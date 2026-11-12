---
name: gramps-import-export-reports
skill_type: skill
description: >-
  Import and export trees and run reports. Do NOT use for tasks outside the gramps-mcp
  connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps import, export and reports

Use the typed tools of the `gramps-mcp` connector: one tool per upstream API operation, named `gramps_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **gramps-people** (`GRAMPS_URL`): holds Person; read with `gramps_get_people`.
- **gramps-families** (`GRAMPS_URL`): holds Family; read with `gramps_get_families`.
- **gramps-events** (`GRAMPS_URL`): holds Event; read with `gramps_get_events`.
- **gramps-places** (`GRAMPS_URL`): holds Place; read with `gramps_get_places`.
- **gramps-sources** (`GRAMPS_URL`): holds Source; read with `gramps_get_sources`.
- **gramps-media** (`GRAMPS_URL`): holds MediaAsset; read with `gramps_get_media_objects`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `gramps-manage-export`

1. `gramps_get_exporter` (`extension`) - Get exporter.
2. `gramps_get_exporter_file` (`extension`) - Get exporter file.
3. `gramps_get_exporter_file_result` (`extension`, `filename`) - Get exporter file result.
4. `gramps_get_exporters` (no parameters) - Get exporters.
5. `gramps_post_exporter_file` (`body`, `extension`) - Post exporter file.

### `gramps-manage-import`

1. `gramps_get_importer` (`extension`) - Get importer.
2. `gramps_get_importers` (no parameters) - Get importers.
3. `gramps_post_importer_file` (`body`, `extension`) - Post importer file. (destructive: ask the operator first)

### `gramps-manage-report`

1. `gramps_get_report` (`report_id`) - Get report.
2. `gramps_get_report_file` (`report_id`) - Get report file.
3. `gramps_get_report_file_result` (`filename`, `report_id`) - Get report file result.
4. `gramps_get_reports` (no parameters) - Get reports.
5. `gramps_post_report_file` (`body`, `report_id`) - Post report file.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
