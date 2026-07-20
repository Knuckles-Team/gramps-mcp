# Gramps MCP

Gramps MCP turns the public Gramps Web API into a typed Python client, a compact MCP
server, and an optional A2A agent. It supports the standard genealogy, evidence, media,
tree, user, import, export, and administrative surfaces without packaging any particular
deployment profile.

Start with:

- [Installation](installation.md) for the MCP and agent extras.
- [Configuration](configuration.md) for AgentConfig, credentials, TLS, and privacy.
- [Usage](usage.md) for Python and MCP examples.
- [Deployment](deployment.md) for stdio, containers, and network exposure.
- [Backing platform](platform.md) for the Gramps instance boundary.

The provider ships neutral capability inputs but no direct graph-write tool. GraphOS
source synchronization requires a centrally compiled and approved signed bundle.
