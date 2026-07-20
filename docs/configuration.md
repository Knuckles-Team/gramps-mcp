# Configuration, trust, and privacy

The package contains connection code and neutral Gramps capability metadata only. Every
endpoint, credential, identity-provider value, trust profile, tree or tenant decision,
and observability destination is supplied at runtime.

## AgentConfig boundary

The MCP entry point calls the shared `load_config()` boundary. AgentConfig projects an
XDG configuration and its approved runtime references into the child process; repository
dotenv files are not a configuration source.

| Setting | Purpose | Durable value |
| --- | --- | --- |
| `GRAMPS_URL` | HTTPS origin of the selected Gramps Web API | Runtime value or alias only |
| `GRAMPS_TOKEN` | Fixed bearer credential when delegation is inactive | Runtime secret only |
| `GRAMPS_USERNAME` / `GRAMPS_PASSWORD` | Optional login pair instead of a token | Runtime secret references only |
| `TLS_PROFILE` / `TLS_PROFILES_REF` | System/private trust, proxy, and optional mTLS | Runtime reference only |
| `MCP_TOOL_MODE` | Condensed, verbose, both, or intent surface | Non-secret deployment choice |

The checked-in `mcp_config.json` uses `env://GRAMPS_URL` and
`env://GRAMPS_TOKEN`. GraphOS can map the aliases through
`MCP_FLEET_SECRET_REFS` to an approved `env://`, `vault://`, or `secret://` source.
A launcher without reference resolution must inject the values itself.

Do not place a literal endpoint, token, username, password, certificate, machine path,
tenant value, or live record in a committed configuration file.

## Authentication

Delegated authentication exchanges the request-scoped identity through the shared RFC
8693 flow and creates a request-specific client. Without delegation, configure either a
fixed token or the complete username/password pair, never both. Token responses,
subjects, emails, credentials, endpoints, and provider response bodies are excluded from
logs and sanitized exceptions.

## TLS

The Gramps origin must be an absolute HTTPS URL without embedded credentials, a query,
or a fragment. The HTTP session is built through
`resolve_configured_tls_profile("gramps")`. Peer and hostname verification are mandatory,
redirects are disabled, and per-request `verify`, certificate, and proxy overrides are
not accepted.

System trust requires no connector-specific option. For a private authority, keep the
complete CA chain or mTLS materials in the runtime trust store, put the catalog behind a
secret reference, and select the profile at deployment time. Never commit certificate
material or disable verification to work around an incomplete chain.

## Genealogy privacy

Apply least privilege and minimum disclosure to living-person records, DNA, family
relationships, dates, places, notes, media, contact details, users, and authentication.
Keep telemetry content capture disabled by default. If OTLP or Langfuse is approved,
export opaque run references, status, counts, timing, and bounded error classes rather
than prompts, responses, tool payloads, records, endpoints, credentials, or paths.

## Governed synchronization

Provider ontology and source presets are unsigned human-authored inputs. They contain no
live records or instance mapping and cannot write to a graph. GraphOS must compile and
sign the exact live capability, then enforce tenant, ACL, consent, classification,
retention, provenance, redaction, and deletion policy before source synchronization.

Validate the boundary without printing resolved values:

```bash
agent-utilities-doctor --only config transport_security mcp_fleet_secrets mcp_fleet
```
