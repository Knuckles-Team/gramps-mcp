---
name: gramps-tree-administration
skill_type: skill
description: >-
  Administer trees and their data: merges, bulk object changes, transactions, background
  tasks, configuration, types, translations, name formats and the search index. Do NOT use
  for tasks outside the gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps tree administration

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

### `gramps-manage-config`

1. `gramps_get_config` (`key`) - Get config.
2. `gramps_get_configs` (no parameters) - Get configs.
3. `gramps_get_tree_config` (`tree_id`) - Get tree config.
4. `gramps_put_config` (`body`, `key`) - Put config.
5. `gramps_put_tree_config` (`body`, `tree_id`) - Put tree config.
6. `gramps_delete_config` (`confirm`, `key`) - Delete config. (destructive: ask the operator first)

### `gramps-inspect-type`

1. `gramps_get_custom_type` (`datatype`) - Get custom type.
2. `gramps_get_custom_types` (no parameters) - Get custom types.
3. `gramps_get_default_type` (`datatype`) - Get default type.
4. `gramps_get_default_type_map` (`datatype`) - Get default type map.
5. `gramps_get_default_types` (no parameters) - Get default types.
6. `gramps_get_types` (no parameters) - Get types.

### `gramps-manage-name-format`

1. `gramps_get_get_name_group` (`surname`) - Get get name group.
2. `gramps_get_name_formats` (no parameters) - Get name formats.
3. `gramps_get_name_groups` (no parameters) - Get name groups.
4. `gramps_get_set_name_group` (`group`, `surname`) - Get set name group.
5. `gramps_post_get_name_group` (`body`, `surname`) - Post get name group.
6. `gramps_post_name_groups` (`body`) - Post name groups.
7. `gramps_post_set_name_group` (`body`, `group`, `surname`) - Post set name group.

### `gramps-manage-merge`

1. `gramps_get_merge_citation` (`phoenix_handle`, `titanic_handle`) - Get merge citation. (destructive: ask the operator first)
2. `gramps_get_merge_event` (`phoenix_handle`, `titanic_handle`) - Get merge event. (destructive: ask the operator first)
3. `gramps_get_merge_media` (`phoenix_handle`, `titanic_handle`) - Get merge media. (destructive: ask the operator first)
4. `gramps_get_merge_note` (`phoenix_handle`, `titanic_handle`) - Get merge note. (destructive: ask the operator first)
5. `gramps_get_merge_place` (`phoenix_handle`, `titanic_handle`) - Get merge place. (destructive: ask the operator first)
6. `gramps_get_merge_repository` (`phoenix_handle`, `titanic_handle`) - Get merge repository. (destructive: ask the operator first)
7. `gramps_get_merge_source` (`phoenix_handle`, `titanic_handle`) - Get merge source. (destructive: ask the operator first)
8. `gramps_post_merge_family` (`body`, `phoenix_handle`, `titanic_handle`) - Post merge family. (destructive: ask the operator first)
9. `gramps_post_merge_person` (`body`, `phoenix_handle`, `titanic_handle`) - Post merge person. (destructive: ask the operator first)

### `gramps-manage-metadata`

1. `gramps_get_metadata` (no parameters) - Get metadata.
2. `gramps_get_metadata_researcher` (no parameters) - Get metadata researcher.
3. `gramps_put_metadata_researcher` (`body`) - Put metadata researcher.

### `gramps-inspect-task`

1. `gramps_get_task` (`task_id`) - Get task.
2. `gramps_get_tasks` (no parameters) - Get tasks.

### `gramps-manage-transaction`

1. `gramps_get_transaction_history` (`transaction_id`) - Get transaction history.
2. `gramps_get_transactions_history` (no parameters) - Get transactions history.
3. `gramps_post_transactions` (`body`) - Post transactions.
4. `gramps_get_transaction_undo` (`transaction_id`) - Get transaction undo. (destructive: ask the operator first)
5. `gramps_post_transaction_undo` (`body`, `transaction_id`) - Post transaction undo. (destructive: ask the operator first)

### `gramps-manage-translation`

1. `gramps_get_translation` (`language`) - Get translation.
2. `gramps_get_translations` (no parameters) - Get translations.
3. `gramps_post_translation` (`body`, `language`) - Post translation.

### `gramps-manage-tree`

1. `gramps_get_tree` (`tree_id`) - Get tree.
2. `gramps_get_trees` (no parameters) - Get trees.
3. `gramps_post_enable_tree` (`body`, `tree_id`) - Post enable tree.
4. `gramps_post_trees` (`body`) - Post trees.
5. `gramps_put_tree` (`body`, `tree_id`) - Put tree.
6. `gramps_post_disable_tree` (`body`, `tree_id`) - Post disable tree. (destructive: ask the operator first)
7. `gramps_post_migrate_tree` (`body`, `tree_id`) - Post migrate tree. (destructive: ask the operator first)
8. `gramps_post_repair_tree` (`body`, `tree_id`) - Post repair tree. (destructive: ask the operator first)

### `gramps-manage-bulk`

1. `gramps_post_objects` (`body`) - Post objects.
2. `gramps_post_delete_objects` (`body`, `confirm`) - Post delete objects. (destructive: ask the operator first)
3. `gramps_post_delete_objects_by_handle` (`body`, `confirm`) - Post delete objects by handle. (destructive: ask the operator first)

### `gramps-manage-index`

1. `gramps_post_search_index` (`body`) - Post search index.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
