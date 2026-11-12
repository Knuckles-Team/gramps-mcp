---
name: gramps-accounts
skill_type: skill
description: >-
  Manage Gramps Web users, tokens, OIDC sign-in and each user's bookmarks. Do NOT use for
  tasks outside the gramps-mcp connector.
license: MIT
tags: [gramps, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Gramps accounts and sign-in

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

### `gramps-manage-bookmark`

1. `gramps_get_bookmark` (`namespace`) - Get bookmark.
2. `gramps_get_bookmarks` (no parameters) - Get bookmarks.
3. `gramps_put_bookmark_edit` (`body`, `handle`, `namespace`) - Put bookmark edit.
4. `gramps_delete_bookmark_edit` (`confirm`, `handle`, `namespace`) - Delete bookmark edit. (destructive: ask the operator first)

### `gramps-manage-user`

1. `gramps_get_user` (`user_name`) - Get user.
2. `gramps_get_users` (no parameters) - Get users.
3. `gramps_get_confirm_email` (no parameters) - Get confirm email.
4. `gramps_get_reset_password` (no parameters) - Get reset password.
5. `gramps_post_change_password` (`body`, `user_name`) - Post change password.
6. `gramps_post_register` (`body`, `user_name`) - Post register.
7. `gramps_post_reset_password` (`body`) - Post reset password.
8. `gramps_post_trigger_reset_password` (`body`, `user_name`) - Post trigger reset password.
9. `gramps_post_user` (`body`, `user_name`) - Post user.
10. `gramps_post_user_create_owner` (`body`, `user_name`) - Post user create owner.
11. `gramps_post_users` (`body`) - Post users.
12. `gramps_post_verify` (`body`, `tree_id`) - Post verify.
13. `gramps_put_user` (`body`, `user_name`) - Put user.
14. `gramps_delete_user` (`confirm`, `user_name`) - Delete user. (destructive: ask the operator first)

### `gramps-manage-oidc`

1. `gramps_get_oidccallbackresource` (no parameters) - Get oidccallbackresource.
2. `gramps_get_oidccallbackresource_provider` (`provider_id`) - Get oidccallbackresource provider.
3. `gramps_get_oidcconfigresource` (no parameters) - Get oidcconfigresource.
4. `gramps_get_oidcloginresource` (no parameters) - Get oidcloginresource.
5. `gramps_get_oidclogoutresource` (no parameters) - Get oidclogoutresource.
6. `gramps_post_oidcbackchannellogoutresource` (`body`) - Post oidcbackchannellogoutresource.

### `gramps-manage-token`

1. `gramps_get_oidctokenexchangeresource` (no parameters) - Get oidctokenexchangeresource.
2. `gramps_get_token_create_owner` (no parameters) - Get token create owner.
3. `gramps_post_token` (`body`) - Post token.
4. `gramps_post_token_create_owner` (`body`) - Post token create owner.
5. `gramps_post_token_refresh` (`body`) - Post token refresh.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Genealogy records can describe living people: never publish or export living persons' details without operator approval.
- Never print or log the Gramps token, username or password.
- Identify records by Gramps handle or id and confirm the record exists before changing, merging or deleting it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
