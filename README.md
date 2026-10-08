# Gramps MCP

## API client | MCP server | A2A agent

![PyPI - Version](https://img.shields.io/pypi/v/gramps-mcp)
![MCP Server](https://badge.mcpx.dev?type=server "MCP Server")
![PyPI - License](https://img.shields.io/pypi/l/gramps-mcp)

*Version: 2.1.0*

`gramps-mcp` exposes the public Gramps Web API as a typed Python client, a compact
action-routed MCP server, and an optional A2A agent. All instance endpoints,
credentials, identity-provider settings, TLS trust, tenant policy, and observability
destinations are provided at runtime.

## Key capabilities

- Thirty-five condensed MCP domains cover people, families, events, places,
  relationships, sources, citations, media, DNA, imports, exports, trees, users, and
  supporting Gramps operations.
- The verbose surface is generated from the vendored OpenAPI operation manifest.
- Blocking HTTP calls are moved off the async MCP event loop through the shared current
  Agent Utilities dispatcher.
- HTTPS peer and hostname verification are mandatory and configured through an
  AgentConfig-backed TLS profile; this package has no boolean verification bypass.
- One complete skill applies research evidence, living-person privacy, and
  read-before-write safety across the complete surface.
- Neutral ontology and source-preset inputs can be compiled centrally into a signed
  GraphOS capability. The provider exposes no direct graph-write tool.

## Available MCP tools

Each condensed tool accepts an `action` plus a JSON string in `params_json`. Domain
toggles are enabled unless a deployment disables them. This table is generated from the
registered server surface.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `gramps_bookmarks` | `BOOKMARKSTOOL` | Manage Gramps bookmarks operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_chat` | `CHATTOOL` | Manage Gramps chat operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_citations` | `CITATIONSTOOL` | Manage Gramps citations operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_config` | `CONFIGTOOL` | Manage Gramps config operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_dna` | `DNATOOL` | Manage Gramps dna operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_events` | `EVENTSTOOL` | Manage Gramps events operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_exporters` | `EXPORTERSTOOL` | Manage Gramps exporters operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_facts` | `FACTSTOOL` | Manage Gramps facts operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_families` | `FAMILIESTOOL` | Manage Gramps families operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_filters` | `FILTERSTOOL` | Manage Gramps filters operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_holidays` | `HOLIDAYSTOOL` | Manage Gramps holidays operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_importers` | `IMPORTERSTOOL` | Manage Gramps importers operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_living` | `LIVINGTOOL` | Manage Gramps living operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_media` | `MEDIATOOL` | Manage Gramps media operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_metadata` | `METADATATOOL` | Manage Gramps metadata operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_name_formats` | `NAME_FORMATSTOOL` | Manage Gramps name formats operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_name_groups` | `NAME_GROUPSTOOL` | Manage Gramps name groups operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_notes` | `NOTESTOOL` | Manage Gramps notes operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_oidc` | `OIDCTOOL` | Manage Gramps oidc operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_people` | `PEOPLETOOL` | Manage Gramps people operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_places` | `PLACESTOOL` | Manage Gramps places operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_relations` | `RELATIONSTOOL` | Manage Gramps relations operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_reports` | `REPORTSTOOL` | Manage Gramps reports operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_repositories` | `REPOSITORIESTOOL` | Manage Gramps repositories operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_search` | `SEARCHTOOL` | Manage Gramps search operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_sources` | `SOURCESTOOL` | Manage Gramps sources operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_tags` | `TAGSTOOL` | Manage Gramps tags operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_tasks` | `TASKSTOOL` | Manage Gramps tasks operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_timeline` | `TIMELINETOOL` | Manage Gramps timeline operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_token` | `TOKENTOOL` | Manage Gramps token operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_transactions` | `TRANSACTIONSTOOL` | Manage Gramps transactions operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_translations` | `TRANSLATIONSTOOL` | Manage Gramps translations operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_trees` | `TREESTOOL` | Manage Gramps trees operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_types` | `TYPESTOOL` | Manage Gramps types operations. CONCEPT:GM-OS.identity.grmp. |
| `gramps_users` | `USERSTOOL` | Manage Gramps users operations. CONCEPT:GM-OS.identity.grmp. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>147 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `gramps_delete_bookmark_edit` | `BOOKMARKSTOOL` | DELETE /bookmarks/{namespace}/{handle} |
| `gramps_delete_config` | `CONFIGTOOL` | DELETE /config/{key}/ |
| `gramps_delete_filter` | `FILTERSTOOL` | DELETE /filters/{namespace}/{name} |
| `gramps_delete_user` | `USERSTOOL` | DELETE /users/{user_name}/ |
| `gramps_get_bookmark` | `BOOKMARKSTOOL` | GET /bookmarks/{namespace} |
| `gramps_get_bookmarks` | `BOOKMARKSTOOL` | GET /bookmarks/ |
| `gramps_get_citation` | `CITATIONSTOOL` | GET /citations/{handle} |
| `gramps_get_citations` | `CITATIONSTOOL` | GET /citations/ |
| `gramps_get_config` | `CONFIGTOOL` | GET /config/{key}/ |
| `gramps_get_configs` | `CONFIGTOOL` | GET /config/ |
| `gramps_get_confirm_email` | `USERSTOOL` | GET /users/-/email/confirm/ |
| `gramps_get_custom_type` | `TYPESTOOL` | GET /types/custom/{datatype} |
| `gramps_get_custom_types` | `TYPESTOOL` | GET /types/custom/ |
| `gramps_get_default_type` | `TYPESTOOL` | GET /types/default/{datatype} |
| `gramps_get_default_type_map` | `TYPESTOOL` | GET /types/default/{datatype}/map |
| `gramps_get_default_types` | `TYPESTOOL` | GET /types/default/ |
| `gramps_get_event` | `EVENTSTOOL` | GET /events/{handle} |
| `gramps_get_event_span` | `EVENTSTOOL` | GET /events/{handle1}/span/{handle2} |
| `gramps_get_events` | `EVENTSTOOL` | GET /events/ |
| `gramps_get_exporter` | `EXPORTERSTOOL` | GET /exporters/{extension} |
| `gramps_get_exporter_file` | `EXPORTERSTOOL` | GET /exporters/{extension}/file |
| `gramps_get_exporter_file_result` | `EXPORTERSTOOL` | GET /exporters/{extension}/file/processed/{filename} |
| `gramps_get_exporters` | `EXPORTERSTOOL` | GET /exporters/ |
| `gramps_get_facts` | `FACTSTOOL` | GET /facts/ |
| `gramps_get_families` | `FAMILIESTOOL` | GET /families/ |
| `gramps_get_family` | `FAMILIESTOOL` | GET /families/{handle} |
| `gramps_get_family_timeline` | `TIMELINETOOL` | GET /families/{handle}/timeline |
| `gramps_get_filter` | `FILTERSTOOL` | GET /filters/{namespace}/{name} |
| `gramps_get_filters` | `FILTERSTOOL` | GET /filters/ |
| `gramps_get_filters_namespace` | `FILTERSTOOL` | GET /filters/{namespace} |
| `gramps_get_get_name_group` | `NAME_GROUPSTOOL` | GET /name-groups/{surname} |
| `gramps_get_holiday` | `HOLIDAYSTOOL` | GET /holidays/{country}/{year}/{month}/{day} |
| `gramps_get_holidays` | `HOLIDAYSTOOL` | GET /holidays/ |
| `gramps_get_importer` | `IMPORTERSTOOL` | GET /importers/{extension} |
| `gramps_get_importers` | `IMPORTERSTOOL` | GET /importers/ |
| `gramps_get_living` | `LIVINGTOOL` | GET /living/{handle} |
| `gramps_get_living_dates` | `LIVINGTOOL` | GET /living/{handle}/dates |
| `gramps_get_media_archive_filename` | `MEDIATOOL` | GET /media/archive/{filename} |
| `gramps_get_media_face_detection` | `MEDIATOOL` | GET /media/{handle}/face_detection |
| `gramps_get_media_file` | `MEDIATOOL` | GET /media/{handle}/file |
| `gramps_get_media_object` | `MEDIATOOL` | GET /media/{handle} |
| `gramps_get_media_objects` | `MEDIATOOL` | GET /media/ |
| `gramps_get_merge_citation` | `CITATIONSTOOL` | GET /citations/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_event` | `EVENTSTOOL` | GET /events/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_media` | `MEDIATOOL` | GET /media/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_note` | `NOTESTOOL` | GET /notes/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_place` | `PLACESTOOL` | GET /places/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_repository` | `REPOSITORIESTOOL` | GET /repositories/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_merge_source` | `SOURCESTOOL` | GET /sources/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_get_metadata` | `METADATATOOL` | GET /metadata/ |
| `gramps_get_metadata_researcher` | `METADATATOOL` | GET /metadata/researcher/ |
| `gramps_get_name_formats` | `NAME_FORMATSTOOL` | GET /name-formats/ |
| `gramps_get_name_groups` | `NAME_GROUPSTOOL` | GET /name-groups/ |
| `gramps_get_note` | `NOTESTOOL` | GET /notes/{handle} |
| `gramps_get_notes` | `NOTESTOOL` | GET /notes/ |
| `gramps_get_oidccallbackresource` | `OIDCTOOL` | GET /oidc/callback/ |
| `gramps_get_oidccallbackresource_provider` | `OIDCTOOL` | GET /oidc/callback/{provider_id} |
| `gramps_get_oidcconfigresource` | `OIDCTOOL` | GET /oidc/config/ |
| `gramps_get_oidcloginresource` | `OIDCTOOL` | GET /oidc/login/ |
| `gramps_get_oidclogoutresource` | `OIDCTOOL` | GET /oidc/logout/ |
| `gramps_get_oidctokenexchangeresource` | `OIDCTOOL` | GET /oidc/tokens/ |
| `gramps_get_people` | `PEOPLETOOL` | GET /people/ |
| `gramps_get_person` | `PEOPLETOOL` | GET /people/{handle} |
| `gramps_get_person_dna_matches` | `DNATOOL` | GET /people/{handle}/dna/matches |
| `gramps_get_person_timeline` | `TIMELINETOOL` | GET /people/{handle}/timeline |
| `gramps_get_person_ydna` | `DNATOOL` | GET /people/{handle}/ydna |
| `gramps_get_place` | `PLACESTOOL` | GET /places/{handle} |
| `gramps_get_places` | `PLACESTOOL` | GET /places/ |
| `gramps_get_relation` | `RELATIONSTOOL` | GET /relations/{handle1}/{handle2} |
| `gramps_get_relations` | `RELATIONSTOOL` | GET /relations/{handle1}/{handle2}/all |
| `gramps_get_report` | `REPORTSTOOL` | GET /reports/{report_id} |
| `gramps_get_report_file` | `REPORTSTOOL` | GET /reports/{report_id}/file |
| `gramps_get_report_file_result` | `REPORTSTOOL` | GET /reports/{report_id}/file/processed/{filename} |
| `gramps_get_reports` | `REPORTSTOOL` | GET /reports/ |
| `gramps_get_repositories` | `REPOSITORIESTOOL` | GET /repositories/ |
| `gramps_get_repository` | `REPOSITORIESTOOL` | GET /repositories/{handle} |
| `gramps_get_reset_password` | `USERSTOOL` | GET /users/-/password/reset/ |
| `gramps_get_search` | `SEARCHTOOL` | GET /search/ |
| `gramps_get_set_name_group` | `NAME_GROUPSTOOL` | GET /name-groups/{surname}/{group} |
| `gramps_get_source` | `SOURCESTOOL` | GET /sources/{handle} |
| `gramps_get_sources` | `SOURCESTOOL` | GET /sources/ |
| `gramps_get_tag` | `TAGSTOOL` | GET /tags/{handle} |
| `gramps_get_tags` | `TAGSTOOL` | GET /tags/ |
| `gramps_get_task` | `TASKSTOOL` | GET /tasks/{task_id} |
| `gramps_get_tasks` | `TASKSTOOL` | GET /tasks/ |
| `gramps_get_timeline_families` | `TIMELINETOOL` | GET /timelines/families/ |
| `gramps_get_timeline_people` | `TIMELINETOOL` | GET /timelines/people/ |
| `gramps_get_token_create_owner` | `TOKENTOOL` | GET /token/create_owner/ |
| `gramps_get_transaction_history` | `TRANSACTIONSTOOL` | GET /transactions/history/{transaction_id} |
| `gramps_get_transaction_undo` | `TRANSACTIONSTOOL` | GET /transactions/history/{transaction_id}/undo |
| `gramps_get_transactions_history` | `TRANSACTIONSTOOL` | GET /transactions/history/ |
| `gramps_get_translation` | `TRANSLATIONSTOOL` | GET /translations/{language} |
| `gramps_get_translations` | `TRANSLATIONSTOOL` | GET /translations/ |
| `gramps_get_tree` | `TREESTOOL` | GET /trees/{tree_id} |
| `gramps_get_tree_config` | `TREESTOOL` | GET /trees/{tree_id}/config |
| `gramps_get_trees` | `TREESTOOL` | GET /trees/ |
| `gramps_get_types` | `TYPESTOOL` | GET /types/ |
| `gramps_get_user` | `USERSTOOL` | GET /users/{user_name}/ |
| `gramps_get_users` | `USERSTOOL` | GET /users/ |
| `gramps_post_change_password` | `USERSTOOL` | POST /users/{user_name}/password/change |
| `gramps_post_chat` | `CHATTOOL` | POST /chat/ |
| `gramps_post_delete_objects` | `TRANSACTIONSTOOL` | POST /objects/delete/ |
| `gramps_post_delete_objects_by_handle` | `TRANSACTIONSTOOL` | POST /objects/delete-by-handle/ |
| `gramps_post_disable_tree` | `TREESTOOL` | POST /trees/{tree_id}/disable |
| `gramps_post_dna_match_parser` | `DNATOOL` | POST /parsers/dna-match |
| `gramps_post_enable_tree` | `TREESTOOL` | POST /trees/{tree_id}/enable |
| `gramps_post_exporter_file` | `EXPORTERSTOOL` | POST /exporters/{extension}/file |
| `gramps_post_families` | `FAMILIESTOOL` | POST /families/ |
| `gramps_post_filters_namespace` | `FILTERSTOOL` | POST /filters/{namespace} |
| `gramps_post_get_name_group` | `NAME_GROUPSTOOL` | POST /name-groups/{surname} |
| `gramps_post_importer_file` | `IMPORTERSTOOL` | POST /importers/{extension}/file |
| `gramps_post_media_archive` | `MEDIATOOL` | POST /media/archive/ |
| `gramps_post_media_archive_upload_zip` | `MEDIATOOL` | POST /media/archive/upload/zip |
| `gramps_post_media_objects` | `MEDIATOOL` | POST /media/ |
| `gramps_post_media_ocr` | `MEDIATOOL` | POST /media/{handle}/ocr |
| `gramps_post_merge_family` | `FAMILIESTOOL` | POST /families/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_post_merge_person` | `PEOPLETOOL` | POST /people/{phoenix_handle}/merge/{titanic_handle} |
| `gramps_post_migrate_tree` | `TREESTOOL` | POST /trees/{tree_id}/migrate |
| `gramps_post_name_groups` | `NAME_GROUPSTOOL` | POST /name-groups/ |
| `gramps_post_objects` | `TRANSACTIONSTOOL` | POST /objects/ |
| `gramps_post_oidcbackchannellogoutresource` | `OIDCTOOL` | POST /oidc/backchannel-logout/ |
| `gramps_post_register` | `USERSTOOL` | POST /users/{user_name}/register/ |
| `gramps_post_repair_tree` | `TREESTOOL` | POST /trees/{tree_id}/repair |
| `gramps_post_report_file` | `REPORTSTOOL` | POST /reports/{report_id}/file |
| `gramps_post_reset_password` | `USERSTOOL` | POST /users/-/password/reset/ |
| `gramps_post_search_index` | `SEARCHTOOL` | POST /search/index/ |
| `gramps_post_set_name_group` | `NAME_GROUPSTOOL` | POST /name-groups/{surname}/{group} |
| `gramps_post_token` | `TOKENTOOL` | POST /token/ |
| `gramps_post_token_create_owner` | `TOKENTOOL` | POST /token/create_owner/ |
| `gramps_post_token_refresh` | `TOKENTOOL` | POST /token/refresh/ |
| `gramps_post_transaction_undo` | `TRANSACTIONSTOOL` | POST /transactions/history/{transaction_id}/undo |
| `gramps_post_transactions` | `TRANSACTIONSTOOL` | POST /transactions/ |
| `gramps_post_translation` | `TRANSLATIONSTOOL` | POST /translations/{language} |
| `gramps_post_trees` | `TREESTOOL` | POST /trees/ |
| `gramps_post_trigger_reset_password` | `USERSTOOL` | POST /users/{user_name}/password/reset/trigger/ |
| `gramps_post_user` | `USERSTOOL` | POST /users/{user_name}/ |
| `gramps_post_user_create_owner` | `USERSTOOL` | POST /users/{user_name}/create_owner/ |
| `gramps_post_users` | `USERSTOOL` | POST /users/ |
| `gramps_post_verify` | `TREESTOOL` | POST /trees/{tree_id}/verify |
| `gramps_put_bookmark_edit` | `BOOKMARKSTOOL` | PUT /bookmarks/{namespace}/{handle} |
| `gramps_put_config` | `CONFIGTOOL` | PUT /config/{key}/ |
| `gramps_put_filters_namespace` | `FILTERSTOOL` | PUT /filters/{namespace} |
| `gramps_put_media_file` | `MEDIATOOL` | PUT /media/{handle}/file |
| `gramps_put_metadata_researcher` | `METADATATOOL` | PUT /metadata/researcher/ |
| `gramps_put_tree` | `TREESTOOL` | PUT /trees/{tree_id} |
| `gramps_put_tree_config` | `TREESTOOL` | PUT /trees/{tree_id}/config |
| `gramps_put_user` | `USERSTOOL` | PUT /users/{user_name}/ |

</details>

_35 action-routed tool(s) · 147 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

| Extra | Installs | Intended use |
| --- | --- | --- |
| `gramps-mcp[mcp]` | Agent Utilities MCP runtime and the mandatory full epistemic-graph base dependency | MCP tool hosting |
| `gramps-mcp[agent]` | Current `agent-runtime` plus Logfire | Integrated A2A agent |
| `gramps-mcp[all]` | MCP and agent runtime | Both entry points |

Run without a durable installation:

```bash
uvx --from "gramps-mcp[mcp]" gramps-mcp
uvx --from "gramps-mcp[agent]" gramps-agent
```

Or install into an environment:

```bash
uv pip install "gramps-mcp[mcp]"
uv pip install "gramps-mcp[agent]"
```

Every install receives `epistemic-graph[full]` through Agent Utilities. The connector
does not start an insecure engine listener or select a machine-specific graph database.
AgentConfig owns engine topology and identity.

## Runtime configuration

The checked-in MCP configuration is reference-only:

```json
{
  "mcpServers": {
    "gramps-mcp": {
      "command": "uvx",
      "args": ["--from", "gramps-mcp[mcp]", "gramps-mcp"],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "GRAMPS_TOKEN": "env://GRAMPS_TOKEN",
        "GRAMPS_URL": "env://GRAMPS_URL"
      }
    }
  }
}
```

An alias-aware GraphOS launcher resolves the two references before creating the child
process. Other launchers must inject the values through their own runtime secret
mechanism. Never replace references with a credential or endpoint in a committed file.

| Setting | Purpose |
| --- | --- |
| `GRAMPS_URL` | Absolute HTTPS origin of the selected Gramps Web API |
| `GRAMPS_TOKEN` | Fixed bearer credential when delegation is inactive |
| `GRAMPS_USERNAME` and `GRAMPS_PASSWORD` | Optional login pair when a fixed token is not used |
| `TLS_PROFILE` / `TLS_PROFILES_REF` | Checked system/private trust and optional mTLS |
| `MCP_TOOL_MODE` | `condensed`, `verbose`, `both`, or `intent` |

The endpoint must not contain credentials, a query, or a fragment. The retired boolean
verification switch is unsupported; trust policy is a resolved TLS profile and cannot
be disabled per request.

Validate configuration without printing resolved values:

```bash
agent-utilities-doctor --only config transport_security mcp_fleet_secrets mcp_fleet
```

## Usage

### Python client

```python
from gramps_mcp.auth import get_client

client = get_client()
try:
    result = client.get_people(page=1, pagesize=25)
    print(result.status_code)
finally:
    client.close()
```

### MCP tool call

```json
{
  "tool": "gramps_people",
  "arguments": {
    "action": "get_people",
    "params_json": "{\"page\":1,\"pagesize\":25}"
  }
}
```

Use `gramps-genealogy-operations` for evidence handling, privacy controls, stable-handle
resolution, and safe mutations. Merges, imports, deletes, tree repair or migration,
transaction undo, user changes, and token/password operations require explicit scope and
approval.

## Containers

The multi-stage Dockerfile provides separate MCP and agent targets:

```bash
docker build --target mcp -t gramps-mcp:mcp -f docker/Dockerfile .
docker build --target agent -t gramps-mcp:agent-local -f docker/Dockerfile .
```

Compose image references, model selection, MCP endpoint, credentials, and telemetry are
externalized. Published ports bind to loopback by default; any wider network exposure
must add authenticated MCP transport, authorization policy, and ingress TLS.

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

The package contributes only provider-owned inputs:

- a mapping of the public Gramps data model;
- neutral people, family, and event source presets;
- one provider skill and canonical prompts;
- entry points that prove which distribution owns each input.

The committed release-generated schema-v2 bundle adds exact local MCP schema
fingerprints, a signed manifest, SHACL shapes, neutral mappings and fixtures, a
migration ledger, and an offline source attestation. It contains no live record,
instance extension, endpoint, credential, local path, tenant mapping, or external-live
claim. Genealogy ingestion also requires approved tenant, ACL, consent, classification,
retention, provenance, redaction, and deletion policy. Missing or stale evidence fails
closed.

Runtime endpoints, credentials, TLS trust, identity, tree/tenant policy, retention, and
observability destinations are deployment inputs and never packaged values. Read
[Configuration, trust, and privacy](docs/configuration.md) before enabling a network
transport, GraphOS delegation, source synchronization, or trace export.
<!-- GOVERNED-CAPABILITY:END -->

## Privacy and observability

Genealogy can expose living-person identities, family relationships, dates, places,
notes, media, DNA, contact details, and authentication data. Keep telemetry content
capture disabled unless a separately approved policy permits it. Export bounded status,
counts, timings, and error classes rather than prompts, responses, tool payloads,
records, endpoints, credentials, or filesystem paths.

See the [documentation](https://knuckles-team.github.io/gramps-mcp/) for configuration,
deployment, and operational guidance.

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | stdio \| streamable-http \| sse |
| `MCP_TOOL_MODE` | `condensed` | condensed \| verbose \| both \| intent |
| `ENABLE_OTEL` | `False` |  |
| `OTEL_EXPORTER_OTLP_HEADERS_REF` | `secret://telemetry/headers` | OTEL_EXPORTER_OTLP_ENDPOINT is supplied at runtime. |
| `LANGFUSE_CAPTURE_CONTENT` | `false` |  |
| `EUNOMIA_TYPE` | `none` | none \| embedded \| remote |
| `BOOKMARKSTOOL` | `True` |  |
| `CHATTOOL` | `True` |  |
| `CITATIONSTOOL` | `True` |  |
| `CONFIGTOOL` | `True` |  |
| `DNATOOL` | `True` |  |
| `EVENTSTOOL` | `True` |  |
| `EXPORTERSTOOL` | `True` |  |
| `FACTSTOOL` | `True` |  |
| `FAMILIESTOOL` | `True` |  |
| `FILTERSTOOL` | `True` |  |
| `HOLIDAYSTOOL` | `True` |  |
| `IMPORTERSTOOL` | `True` |  |
| `LIVINGTOOL` | `True` |  |
| `MEDIATOOL` | `True` |  |
| `METADATATOOL` | `True` |  |
| `NAME_FORMATSTOOL` | `True` |  |
| `NAME_GROUPSTOOL` | `True` |  |
| `NOTESTOOL` | `True` |  |
| `OIDCTOOL` | `True` |  |
| `PEOPLETOOL` | `True` |  |
| `PLACESTOOL` | `True` |  |
| `RELATIONSTOOL` | `True` |  |
| `REPORTSTOOL` | `True` |  |
| `REPOSITORIESTOOL` | `True` |  |
| `SEARCHTOOL` | `True` |  |
| `SOURCESTOOL` | `True` |  |
| `TAGSTOOL` | `True` |  |
| `TASKSTOOL` | `True` |  |
| `TIMELINETOOL` | `True` |  |
| `TOKENTOOL` | `True` |  |
| `TRANSACTIONSTOOL` | `True` |  |
| `TRANSLATIONSTOOL` | `True` |  |
| `TREESTOOL` | `True` |  |
| `TYPESTOOL` | `True` |  |
| `USERSTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` | Embedded Eunomia policy file |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | — | Operator-configured LLM provider for the agent |
| `MODEL_ID` | — | Operator-configured model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_43 package + 18 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `gramps-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "gramps-mcp[mcp]"`, then run `gramps-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `gramps-mcp` |
| Immutable container | deploy `registry.example.invalid/gramps-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->
