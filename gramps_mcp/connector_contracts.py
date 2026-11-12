"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "gramps-manage-bookmark",
        (
            ToolStep(
                "gramps_get_bookmark",
                params=("namespace",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_bookmarks",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_put_bookmark_edit",
                params=(
                    "body",
                    "handle",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_bookmark_edit",
                params=(
                    "confirm",
                    "handle",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-user",
        (
            ToolStep(
                "gramps_get_user",
                params=("user_name",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_users",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_confirm_email",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_reset_password",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_change_password",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_register",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_reset_password",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_trigger_reset_password",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_user",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_user_create_owner",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_users",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_verify",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_user",
                params=(
                    "body",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_user",
                params=(
                    "confirm",
                    "user_name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-oidc",
        (
            ToolStep(
                "gramps_get_oidccallbackresource",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_oidccallbackresource_provider",
                params=("provider_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_oidcconfigresource",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_oidcloginresource",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_oidclogoutresource",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_oidcbackchannellogoutresource",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-token",
        (
            ToolStep(
                "gramps_get_oidctokenexchangeresource",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_token_create_owner",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_token",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_token_create_owner",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_token_refresh",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-config",
        (
            ToolStep(
                "gramps_get_config",
                params=("key",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_configs",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_tree_config",
                params=("tree_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_put_config",
                params=(
                    "body",
                    "key",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_tree_config",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_config",
                params=(
                    "confirm",
                    "key",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-type",
        (
            ToolStep(
                "gramps_get_custom_type",
                params=("datatype",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_custom_types",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_default_type",
                params=("datatype",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_default_type_map",
                params=("datatype",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_default_types",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_types",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-name-format",
        (
            ToolStep(
                "gramps_get_get_name_group",
                params=("surname",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_name_formats",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_name_groups",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_set_name_group",
                params=(
                    "group",
                    "surname",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_get_name_group",
                params=(
                    "body",
                    "surname",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_name_groups",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_set_name_group",
                params=(
                    "body",
                    "group",
                    "surname",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-merge",
        (
            ToolStep(
                "gramps_get_merge_citation",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_event",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_media",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_note",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_place",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_repository",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_merge_source",
                params=(
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_merge_family",
                params=(
                    "body",
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_merge_person",
                params=(
                    "body",
                    "phoenix_handle",
                    "titanic_handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-metadata",
        (
            ToolStep(
                "gramps_get_metadata",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_metadata_researcher",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_put_metadata_researcher",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-task",
        (
            ToolStep(
                "gramps_get_task",
                params=("task_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_tasks",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-transaction",
        (
            ToolStep(
                "gramps_get_transaction_history",
                params=("transaction_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_transactions_history",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_transactions",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_get_transaction_undo",
                params=("transaction_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_transaction_undo",
                params=(
                    "body",
                    "transaction_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-translation",
        (
            ToolStep(
                "gramps_get_translation",
                params=("language",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_translations",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_translation",
                params=(
                    "body",
                    "language",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-tree",
        (
            ToolStep(
                "gramps_get_tree",
                params=("tree_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_trees",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_enable_tree",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_trees",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_tree",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_disable_tree",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_migrate_tree",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_repair_tree",
                params=(
                    "body",
                    "tree_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-bulk",
        (
            ToolStep(
                "gramps_post_objects",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_delete_objects",
                params=(
                    "body",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_delete_objects_by_handle",
                params=(
                    "body",
                    "confirm",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-index",
        (
            ToolStep(
                "gramps_post_search_index",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-object",
        (
            ToolStep(
                "gramps_get_media_object",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_media_objects",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_media_objects",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_media_object",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_media_object",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-file",
        (
            ToolStep(
                "gramps_get_media_archive_filename",
                params=("filename",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_media_file",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_media_archive",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_post_media_archive_upload_zip",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_media_file",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-analysis",
        (
            ToolStep(
                "gramps_get_media_face_detection",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_media_ocr",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-export",
        (
            ToolStep(
                "gramps_get_exporter",
                params=("extension",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_exporter_file",
                params=("extension",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_exporter_file_result",
                params=(
                    "extension",
                    "filename",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_exporters",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_exporter_file",
                params=(
                    "body",
                    "extension",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-import",
        (
            ToolStep(
                "gramps_get_importer",
                params=("extension",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_importers",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_importer_file",
                params=(
                    "body",
                    "extension",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-report",
        (
            ToolStep(
                "gramps_get_report",
                params=("report_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_report_file",
                params=("report_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_report_file_result",
                params=(
                    "filename",
                    "report_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_reports",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_report_file",
                params=(
                    "body",
                    "report_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-filter",
        (
            ToolStep(
                "gramps_get_filter",
                params=(
                    "name",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_filters",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_filters_namespace",
                params=("namespace",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_filters_namespace",
                params=(
                    "body",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_put_filters_namespace",
                params=(
                    "body",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_filter",
                params=(
                    "confirm",
                    "name",
                    "namespace",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-fact",
        (
            ToolStep(
                "gramps_get_facts",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-timeline",
        (
            ToolStep(
                "gramps_get_family_timeline",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_person_timeline",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_timeline_families",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_timeline_people",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-holiday",
        (
            ToolStep(
                "gramps_get_holiday",
                params=(
                    "country",
                    "day",
                    "month",
                    "year",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_holidays",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-living",
        (
            ToolStep(
                "gramps_get_living",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_living_dates",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-dna",
        (
            ToolStep(
                "gramps_get_person_dna_matches",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_person_ydna",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_dna_match_parser",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-relation",
        (
            ToolStep(
                "gramps_get_relation",
                params=(
                    "handle1",
                    "handle2",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_relations",
                params=(
                    "handle1",
                    "handle2",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-search",
        (
            ToolStep(
                "gramps_get_search",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-inspect-chat",
        (
            ToolStep(
                "gramps_post_chat",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-citation",
        (
            ToolStep(
                "gramps_get_citation",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_citations",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_citations",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_citation",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_citation",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-note",
        (
            ToolStep(
                "gramps_get_note",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_notes",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_notes",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_note",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_note",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-repository",
        (
            ToolStep(
                "gramps_get_repositories",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_repository",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_repositories",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_repository",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_repository",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-source",
        (
            ToolStep(
                "gramps_get_source",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_sources",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_sources",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_source",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_source",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-tag",
        (
            ToolStep(
                "gramps_get_tag",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_tags",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_tags",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_tag",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_tag",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-event",
        (
            ToolStep(
                "gramps_get_event",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_event_span",
                params=(
                    "handle1",
                    "handle2",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_events",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_events",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_event",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_event",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-family",
        (
            ToolStep(
                "gramps_get_families",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_family",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_families",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_family",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_family",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-person",
        (
            ToolStep(
                "gramps_get_people",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_person",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_people",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_person",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_person",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "gramps-manage-place",
        (
            ToolStep(
                "gramps_get_place",
                params=("handle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_get_places",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "gramps_post_places",
                params=("body",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_put_place",
                params=(
                    "body",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "gramps_delete_place",
                params=(
                    "confirm",
                    "handle",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "gramps-manage-bookmark",
        tools=(
            "gramps_delete_bookmark_edit",
            "gramps_get_bookmark",
            "gramps_get_bookmarks",
            "gramps_put_bookmark_edit",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-account-manager",
        ),
        skills=("gramps-accounts",),
    ),
    SurfaceLink(
        "gramps-manage-user",
        tools=(
            "gramps_delete_user",
            "gramps_get_confirm_email",
            "gramps_get_reset_password",
            "gramps_get_user",
            "gramps_get_users",
            "gramps_post_change_password",
            "gramps_post_register",
            "gramps_post_reset_password",
            "gramps_post_trigger_reset_password",
            "gramps_post_user",
            "gramps_post_user_create_owner",
            "gramps_post_users",
            "gramps_post_verify",
            "gramps_put_user",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-account-manager",
        ),
        skills=("gramps-accounts",),
    ),
    SurfaceLink(
        "gramps-manage-oidc",
        tools=(
            "gramps_get_oidccallbackresource",
            "gramps_get_oidccallbackresource_provider",
            "gramps_get_oidcconfigresource",
            "gramps_get_oidcloginresource",
            "gramps_get_oidclogoutresource",
            "gramps_post_oidcbackchannellogoutresource",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-account-manager",
        ),
        skills=("gramps-accounts",),
    ),
    SurfaceLink(
        "gramps-manage-token",
        tools=(
            "gramps_get_oidctokenexchangeresource",
            "gramps_get_token_create_owner",
            "gramps_post_token",
            "gramps_post_token_create_owner",
            "gramps_post_token_refresh",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-account-manager",
        ),
        skills=("gramps-accounts",),
    ),
    SurfaceLink(
        "gramps-manage-config",
        tools=(
            "gramps_delete_config",
            "gramps_get_config",
            "gramps_get_configs",
            "gramps_get_tree_config",
            "gramps_put_config",
            "gramps_put_tree_config",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-inspect-type",
        tools=(
            "gramps_get_custom_type",
            "gramps_get_custom_types",
            "gramps_get_default_type",
            "gramps_get_default_type_map",
            "gramps_get_default_types",
            "gramps_get_types",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-name-format",
        tools=(
            "gramps_get_get_name_group",
            "gramps_get_name_formats",
            "gramps_get_name_groups",
            "gramps_get_set_name_group",
            "gramps_post_get_name_group",
            "gramps_post_name_groups",
            "gramps_post_set_name_group",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-merge",
        tools=(
            "gramps_get_merge_citation",
            "gramps_get_merge_event",
            "gramps_get_merge_media",
            "gramps_get_merge_note",
            "gramps_get_merge_place",
            "gramps_get_merge_repository",
            "gramps_get_merge_source",
            "gramps_post_merge_family",
            "gramps_post_merge_person",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-metadata",
        tools=(
            "gramps_get_metadata",
            "gramps_get_metadata_researcher",
            "gramps_put_metadata_researcher",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-inspect-task",
        tools=(
            "gramps_get_task",
            "gramps_get_tasks",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-transaction",
        tools=(
            "gramps_get_transaction_history",
            "gramps_get_transaction_undo",
            "gramps_get_transactions_history",
            "gramps_post_transaction_undo",
            "gramps_post_transactions",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-translation",
        tools=(
            "gramps_get_translation",
            "gramps_get_translations",
            "gramps_post_translation",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-tree",
        tools=(
            "gramps_get_tree",
            "gramps_get_trees",
            "gramps_post_disable_tree",
            "gramps_post_enable_tree",
            "gramps_post_migrate_tree",
            "gramps_post_repair_tree",
            "gramps_post_trees",
            "gramps_put_tree",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-bulk",
        tools=(
            "gramps_post_delete_objects",
            "gramps_post_delete_objects_by_handle",
            "gramps_post_objects",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-index",
        tools=("gramps_post_search_index",),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-tree-administration",),
    ),
    SurfaceLink(
        "gramps-manage-object",
        tools=(
            "gramps_delete_media_object",
            "gramps_get_media_object",
            "gramps_get_media_objects",
            "gramps_post_media_objects",
            "gramps_put_media_object",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-media-archivist",
        ),
        skills=("gramps-media-management",),
    ),
    SurfaceLink(
        "gramps-manage-file",
        tools=(
            "gramps_get_media_archive_filename",
            "gramps_get_media_file",
            "gramps_post_media_archive",
            "gramps_post_media_archive_upload_zip",
            "gramps_put_media_file",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-media-archivist",
        ),
        skills=("gramps-media-management",),
    ),
    SurfaceLink(
        "gramps-manage-analysis",
        tools=(
            "gramps_get_media_face_detection",
            "gramps_post_media_ocr",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-media-archivist",
        ),
        skills=("gramps-media-management",),
    ),
    SurfaceLink(
        "gramps-manage-export",
        tools=(
            "gramps_get_exporter",
            "gramps_get_exporter_file",
            "gramps_get_exporter_file_result",
            "gramps_get_exporters",
            "gramps_post_exporter_file",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-import-export-reports",),
    ),
    SurfaceLink(
        "gramps-manage-import",
        tools=(
            "gramps_get_importer",
            "gramps_get_importers",
            "gramps_post_importer_file",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-import-export-reports",),
    ),
    SurfaceLink(
        "gramps-manage-report",
        tools=(
            "gramps_get_report",
            "gramps_get_report_file",
            "gramps_get_report_file_result",
            "gramps_get_reports",
            "gramps_post_report_file",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-tree-administrator",
        ),
        skills=("gramps-import-export-reports",),
    ),
    SurfaceLink(
        "gramps-manage-filter",
        tools=(
            "gramps_delete_filter",
            "gramps_get_filter",
            "gramps_get_filters",
            "gramps_get_filters_namespace",
            "gramps_post_filters_namespace",
            "gramps_put_filters_namespace",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-fact",
        tools=("gramps_get_facts",),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-timeline",
        tools=(
            "gramps_get_family_timeline",
            "gramps_get_person_timeline",
            "gramps_get_timeline_families",
            "gramps_get_timeline_people",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-holiday",
        tools=(
            "gramps_get_holiday",
            "gramps_get_holidays",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-living",
        tools=(
            "gramps_get_living",
            "gramps_get_living_dates",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-dna",
        tools=(
            "gramps_get_person_dna_matches",
            "gramps_get_person_ydna",
            "gramps_post_dna_match_parser",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-relation",
        tools=(
            "gramps_get_relation",
            "gramps_get_relations",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-search",
        tools=("gramps_get_search",),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-inspect-chat",
        tools=("gramps_post_chat",),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-search-and-analysis",),
    ),
    SurfaceLink(
        "gramps-manage-citation",
        tools=(
            "gramps_delete_citation",
            "gramps_get_citation",
            "gramps_get_citations",
            "gramps_post_citations",
            "gramps_put_citation",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-source-records",),
    ),
    SurfaceLink(
        "gramps-manage-note",
        tools=(
            "gramps_delete_note",
            "gramps_get_note",
            "gramps_get_notes",
            "gramps_post_notes",
            "gramps_put_note",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-source-records",),
    ),
    SurfaceLink(
        "gramps-manage-repository",
        tools=(
            "gramps_delete_repository",
            "gramps_get_repositories",
            "gramps_get_repository",
            "gramps_post_repositories",
            "gramps_put_repository",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-source-records",),
    ),
    SurfaceLink(
        "gramps-manage-source",
        tools=(
            "gramps_delete_source",
            "gramps_get_source",
            "gramps_get_sources",
            "gramps_post_sources",
            "gramps_put_source",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-source-records",),
    ),
    SurfaceLink(
        "gramps-manage-tag",
        tools=(
            "gramps_delete_tag",
            "gramps_get_tag",
            "gramps_get_tags",
            "gramps_post_tags",
            "gramps_put_tag",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-source-records",),
    ),
    SurfaceLink(
        "gramps-manage-event",
        tools=(
            "gramps_delete_event",
            "gramps_get_event",
            "gramps_get_event_span",
            "gramps_get_events",
            "gramps_post_events",
            "gramps_put_event",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-family-records",),
    ),
    SurfaceLink(
        "gramps-manage-family",
        tools=(
            "gramps_delete_family",
            "gramps_get_families",
            "gramps_get_family",
            "gramps_post_families",
            "gramps_put_family",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-family-records",),
    ),
    SurfaceLink(
        "gramps-manage-person",
        tools=(
            "gramps_delete_person",
            "gramps_get_people",
            "gramps_get_person",
            "gramps_post_people",
            "gramps_put_person",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-family-records",),
    ),
    SurfaceLink(
        "gramps-manage-place",
        tools=(
            "gramps_delete_place",
            "gramps_get_place",
            "gramps_get_places",
            "gramps_post_places",
            "gramps_put_place",
        ),
        prompts=(
            "genealogy_specialist",
            "gramps-genealogist",
        ),
        skills=("gramps-family-records",),
    ),
    SurfaceLink(
        "gramps-genealogy-operations",
        tools=(
            "gramps_get_person",
            "gramps_post_tags",
        ),
        prompts=("genealogy_specialist",),
        skills=("gramps-genealogy-operations",),
    ),
    SurfaceLink(
        "gramps-genealogy-research",
        tools=(
            "gramps_delete_person",
            "gramps_get_event",
            "gramps_get_event_span",
            "gramps_get_events",
            "gramps_get_families",
            "gramps_get_family",
            "gramps_get_family_timeline",
            "gramps_get_people",
            "gramps_get_person",
            "gramps_get_person_timeline",
            "gramps_get_relation",
            "gramps_get_relations",
            "gramps_get_search",
            "gramps_post_merge_family",
            "gramps_post_merge_person",
            "gramps_post_people",
            "gramps_put_person",
        ),
        prompts=("genealogy_specialist",),
        skills=("gramps-genealogy-research",),
    ),
    SurfaceLink(
        "gramps-media-archive",
        tools=(
            "gramps_get_media_face_detection",
            "gramps_get_media_file",
            "gramps_get_media_object",
            "gramps_get_media_objects",
            "gramps_post_media_archive",
            "gramps_post_media_ocr",
        ),
        prompts=("genealogy_specialist",),
        skills=("gramps-media-archive",),
    ),
    SurfaceLink(
        "gramps-tree-ingestion",
        tools=(
            "gramps_get_events",
            "gramps_get_families",
            "gramps_get_people",
        ),
        prompts=("genealogy_specialist",),
        skills=("gramps-tree-ingestion",),
    ),
)

LOCATIONS = (
    DataLocation(
        "gramps-people",
        ("Person",),
        "GRAMPS_URL",
        "gramps_get_people",
    ),
    DataLocation(
        "gramps-families",
        ("Family",),
        "GRAMPS_URL",
        "gramps_get_families",
    ),
    DataLocation(
        "gramps-events",
        ("Event",),
        "GRAMPS_URL",
        "gramps_get_events",
    ),
    DataLocation(
        "gramps-places",
        ("Place",),
        "GRAMPS_URL",
        "gramps_get_places",
    ),
    DataLocation(
        "gramps-sources",
        ("Source",),
        "GRAMPS_URL",
        "gramps_get_sources",
    ),
    DataLocation(
        "gramps-media",
        ("MediaAsset",),
        "GRAMPS_URL",
        "gramps_get_media_objects",
    ),
)

ROLES = (
    BusinessRole(
        "genealogist",
        tasks=(
            "gramps-inspect-chat",
            "gramps-inspect-dna",
            "gramps-inspect-fact",
            "gramps-inspect-holiday",
            "gramps-inspect-living",
            "gramps-inspect-relation",
            "gramps-inspect-search",
            "gramps-inspect-timeline",
            "gramps-manage-citation",
            "gramps-manage-event",
            "gramps-manage-family",
            "gramps-manage-filter",
            "gramps-manage-note",
            "gramps-manage-person",
            "gramps-manage-place",
            "gramps-manage-repository",
            "gramps-manage-source",
            "gramps-manage-tag",
        ),
    ),
    BusinessRole(
        "media archivist",
        tasks=(
            "gramps-manage-analysis",
            "gramps-manage-file",
            "gramps-manage-object",
        ),
    ),
    BusinessRole(
        "tree administrator",
        tasks=(
            "gramps-inspect-task",
            "gramps-inspect-type",
            "gramps-manage-bulk",
            "gramps-manage-config",
            "gramps-manage-export",
            "gramps-manage-import",
            "gramps-manage-index",
            "gramps-manage-merge",
            "gramps-manage-metadata",
            "gramps-manage-name-format",
            "gramps-manage-report",
            "gramps-manage-transaction",
            "gramps-manage-translation",
            "gramps-manage-tree",
        ),
    ),
    BusinessRole(
        "account manager",
        tasks=(
            "gramps-manage-bookmark",
            "gramps-manage-oidc",
            "gramps-manage-token",
            "gramps-manage-user",
        ),
    ),
)
