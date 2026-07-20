# Deployment

## Local stdio child

Use the reference-only `mcp_config.json` with an alias-aware launcher. It installs the
MCP extra through `uvx`, selects the condensed surface, and expects runtime aliases for
the endpoint and credential. A non-alias-aware launcher must inject those values through
its own secret mechanism.

## Containers

`docker/mcp.compose.yml` runs only the MCP server. `docker/agent.compose.yml` adds the
current A2A runtime. Image names are externalized through `GRAMPS_MCP_IMAGE` and
`GRAMPS_AGENT_IMAGE`; the agent also requires runtime `MCP_URL`, `PROVIDER`, and
`MODEL_ID` values.

The multi-stage image installs the checked-out package source and drops to an
unprivileged runtime user. Compose injects endpoint, credential or secret reference,
and TLS-profile selectors from the launch environment; it does not read a repository
dotenv file.

Published ports bind to loopback by default. Keep telemetry and the web UI disabled
unless explicitly approved. The compose files do not deploy a Gramps database,
identity provider, graph database, or observability backend.

## Network MCP

When using streamable HTTP or SSE:

1. Terminate TLS at an approved ingress or configure the server transport directly.
2. Require MCP client authentication and authorization.
3. Limit the listener and ingress to intended callers.
4. Apply request, response, and rate limits appropriate for genealogy exports and media.
5. Keep provider credentials and TLS profiles behind runtime references.

Do not expose the container listener broadly merely because the internal process binds
to all container interfaces.

## Readiness

Container health checks are local and content-free. For an authorized deployed A2A
service, run `scripts/validate_a2a_agent.py --url <https-endpoint>`; it uses the shared
TLS profile, disables redirects, sends a bounded readiness prompt, and prints no endpoint
or response content.
