---
name: gramps-search-and-analysis
skill_type: skill
description: >-
  Search, filter and analyse the tree: relationships, living status, timelines, facts,
  holidays, DNA matches and the genealogy assistant. Do NOT use for tasks outside the
  gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps search and analysis

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

### `gramps-manage-filter`

1. `gramps_get_filter` (`name`, `namespace`) - Get filter.
2. `gramps_get_filters` (no parameters) - Get filters.
3. `gramps_get_filters_namespace` (`namespace`) - Get filters namespace.
4. `gramps_post_filters_namespace` (`body`, `namespace`) - Post filters namespace.
5. `gramps_put_filters_namespace` (`body`, `namespace`) - Put filters namespace.
6. `gramps_delete_filter` (`confirm`, `name`, `namespace`) - Delete filter. (destructive: ask the operator first)

### `gramps-inspect-fact`

1. `gramps_get_facts` (no parameters) - Get facts.

### `gramps-inspect-timeline`

1. `gramps_get_family_timeline` (`handle`) - Get family timeline.
2. `gramps_get_person_timeline` (`handle`) - Get person timeline.
3. `gramps_get_timeline_families` (no parameters) - Get timeline families.
4. `gramps_get_timeline_people` (no parameters) - Get timeline people.

### `gramps-inspect-holiday`

1. `gramps_get_holiday` (`country`, `day`, `month`, `year`) - Get holiday.
2. `gramps_get_holidays` (no parameters) - Get holidays.

### `gramps-inspect-living`

1. `gramps_get_living` (`handle`) - Get living.
2. `gramps_get_living_dates` (`handle`) - Get living dates.

### `gramps-inspect-dna`

1. `gramps_get_person_dna_matches` (`handle`) - Get person dna matches.
2. `gramps_get_person_ydna` (`handle`) - Get person ydna.
3. `gramps_post_dna_match_parser` (`body`) - Post dna match parser.

### `gramps-inspect-relation`

1. `gramps_get_relation` (`handle1`, `handle2`) - Get relation.
2. `gramps_get_relations` (`handle1`, `handle2`) - Get relations.

### `gramps-inspect-search`

1. `gramps_get_search` (no parameters) - Get search.

### `gramps-inspect-chat`

1. `gramps_post_chat` (`body`) - Post chat.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
