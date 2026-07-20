# Backing platform

Gramps MCP connects to an operator-managed Gramps Web API. It does not install or modify
that service, choose a tree, create an owner, or infer a deployment topology.

Provide the HTTPS origin and one supported authentication path through AgentConfig:

- delegated identity when the Gramps and identity-provider deployment supports it;
- a scoped fixed bearer token; or
- a runtime username/password pair exchanged for short-lived tokens.

Use the smallest Gramps role required by enabled domains. Administrative surfaces such
as users, tokens, configuration, trees, imports, transactions, and owner creation should
normally be disabled for research-only deployments.

Private trust and mTLS belong to the shared TLS profile, not to provider code. A Gramps
instance with custom data or plugins remains usable through its public API, but this
repository does not store customized instance schemas or mappings. Live capability
discovery and mapping belong to the central governed compiler.
