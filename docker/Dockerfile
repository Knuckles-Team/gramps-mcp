# syntax=docker/dockerfile:1
# Two right-sized images from ONE Dockerfile, selected by build --target. Both are
# slim multi-stage (build in a builder, ship only /usr/local — no dev-tools/source):
#
#   --target agent  (DEFAULT)  installs gramps-mcp[agent] = the current runtime
#                              (agent-utilities[agent-runtime]: full engine + pydantic-ai +
#                              skills). Because the closure also includes MCP, this image
#                              can run EITHER the agent OR the mcp server. Push as the
#                              default tags: latest / main / <version>.
#
#   --target mcp               installs gramps-mcp[mcp] = MCP-server tooling without
#                              the agent UI/runtime. The mandatory epistemic-graph[full]
#                              base dependency remains present.
#
#   docker build --target agent -t gramps-mcp:agent-local .
#   docker build --target mcp   -t gramps-mcp:mcp    .
FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6 AS builder-base
COPY --from=ghcr.io/astral-sh/uv:0.11.7@sha256:240fb85ab0f263ef12f492d8476aa3a2e4e1e333f7d67fbdd923d00a506a516a /uv /uvx /bin/
WORKDIR /src
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_SYSTEM_PYTHON=1 \
    UV_HTTP_TIMEOUT=3600
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
COPY . /src

# Slim MCP-only dependency closure.
FROM builder-base AS builder-mcp
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --upgrade --break-system-packages ".[mcp]"

# Full agent runtime dependency closure.
FROM builder-base AS builder-agent
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --upgrade --break-system-packages ".[agent]"

FROM python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6 AS runtime-base
ARG HOST=0.0.0.0
ARG PORT=8000
ARG TRANSPORT="stdio"
ARG AUTH_TYPE="none"
ENV HOST=${HOST} \
    PORT=${PORT} \
    TRANSPORT=${TRANSPORT} \
    AUTH_TYPE=${AUTH_TYPE} \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:/usr/local/bin:${PATH}" \
    UV_HTTP_TIMEOUT=3600 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    HOME=/home/gramps \
    XDG_CONFIG_HOME=/home/gramps/.config \
    XDG_CACHE_HOME=/home/gramps/.cache \
    XDG_STATE_HOME=/home/gramps/.local/state \
    XDG_RUNTIME_DIR=/tmp/gramps-runtime
RUN groupadd --system --gid 10001 gramps \
    && useradd --system --uid 10001 --gid gramps --home-dir /home/gramps gramps \
    && install -d -o gramps -g gramps -m 0700 \
        /home/gramps/.config \
        /home/gramps/.cache \
        /home/gramps/.local/state \
        /tmp/gramps-runtime
USER gramps

# Slim image: MCP server only.
FROM runtime-base AS mcp
COPY --from=builder-mcp /usr/local /usr/local
CMD ["gramps-mcp"]

# Full image (DEFAULT target): agent runtime; can also run the mcp server.
FROM runtime-base AS agent
COPY --from=builder-agent /usr/local /usr/local
CMD ["gramps-agent"]
