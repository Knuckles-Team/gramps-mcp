#!/usr/bin/env python
"""Generate the Gramps API client + MCP tools from the vendored OpenAPI spec.

This is an **author-time** developer tool, not a runtime dependency. It reads the
spec(s) in ``gramps_mcp/specs/*.json`` and emits fleet-conformant, committed
code:

* ``gramps_mcp/api/api_client_<domain>.py`` — one method per OpenAPI operation,
  composed into ``gramps_mcp.api_client.Api`` via multiple inheritance.
* ``gramps_mcp/api/_operation_manifest.py`` — the machine-readable
  ``operationId → method → action`` map that the coverage test asserts against and
  that drives the verbose 1:1 tool tier.
* ``gramps_mcp/mcp/mcp_<domain>.py`` — one consolidated, action-routed MCP tool
  per domain exposing every operation as an ``action``.
* ``gramps_mcp/mcp/__init__.py`` — ``TOOL_REGISTRY`` consumed by ``mcp_server.py``.
* ``gramps_mcp/api_client.py`` — the composite ``Api`` class.

The OpenAPI spec is derived from the documented Gramps REST routes
(``gramps-project/gramps-web-api``) — see ``gramps_mcp/specs/``.

Re-run after refreshing the specs:  ``python scripts/generate_from_openapi.py``
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent / "gramps_mcp"
SPECS_DIR = PKG / "specs"
API_DIR = PKG / "api"
MCP_DIR = PKG / "mcp"

HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def snake(name: str) -> str:
    """Convert an operationId / slug / tag to a safe snake_case Python identifier."""
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    if not name:
        name = "op"
    if name[0].isdigit():
        name = "op_" + name
    if keyword.iskeyword(name):
        name += "_"
    return name


def camel(domain: str) -> str:
    return "".join(part.capitalize() for part in domain.split("_"))


def server_template(spec: dict) -> str:
    servers = spec.get("servers") or [{}]
    return servers[0].get("url", "").rstrip("/")


def detect_pagination(http: str, query_params: list[str]) -> str:
    if http.upper() != "GET":
        return "none"
    qs = set(query_params)
    if "page" in qs and ("pagesize" in qs or "per_page" in qs):
        return "offset"
    return "none"


_OPENAPI_SCALAR = {"string", "integer", "number", "boolean", "array", "object"}


def _resolve_ref(spec: dict, node):
    seen: set[str] = set()
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/") or ref in seen:
            break
        seen.add(ref)
        cur = spec
        for part in ref[2:].split("/"):
            cur = cur.get(part, {}) if isinstance(cur, dict) else {}
        node = cur
    return node if isinstance(node, dict) else {}


def _param_entry(name: str, schema: dict, required: bool, description) -> dict:
    schema = schema or {}
    t = schema.get("type")
    if not t and any(k in schema for k in ("$ref", "allOf", "properties")):
        t = "object"
    if t not in _OPENAPI_SCALAR:
        t = "string"
    return {
        "name": name,
        "type": t,
        "required": bool(required),
        "description": re.sub(r"\s+", " ", (description or "").strip())[:200],
    }


def normalize_params(params: list, op: dict, spec: dict) -> list[dict]:
    """Flatten path/query params + top-level requestBody fields into typed entries."""
    out: list[dict] = []
    seen: set[str] = set()
    for p in params:
        p = _resolve_ref(spec, p)
        name = p.get("name")
        if not name or p.get("in") not in ("path", "query") or name in seen:
            continue
        seen.add(name)
        out.append(
            _param_entry(
                name,
                p.get("schema") or {},
                p.get("required") or p.get("in") == "path",
                p.get("description"),
            )
        )
    request_body = _resolve_ref(spec, op.get("requestBody") or {})
    if request_body:
        content = request_body.get("content") or {}
        media: dict = content.get("application/json") or next(
            iter(content.values()), {}
        )
        schema = _resolve_ref(spec, (media or {}).get("schema") or {})
        props = schema.get("properties") or {}
        required = set(schema.get("required") or [])
        if props:
            for pname, pschema in props.items():
                if pname in seen:
                    continue
                seen.add(pname)
                ps = _resolve_ref(spec, pschema)
                out.append(
                    _param_entry(pname, ps, pname in required, ps.get("description"))
                )
        else:
            out.append(
                {
                    "name": "body",
                    "type": "object",
                    "required": bool(request_body.get("required")),
                    "description": "Request body (JSON object).",
                }
            )
    return out


def collect_operations() -> dict[str, list[dict]]:
    """Return ``{domain: [operation_meta, ...]}`` across all vendored specs."""
    by_domain: dict[str, list[dict]] = {}
    global_methods: set[str] = set()
    synthetic = 0

    for spec_path in sorted(SPECS_DIR.glob("*.json")):
        spec = json.loads(spec_path.read_text())
        base = server_template(spec)

        for path, methods in (spec.get("paths") or {}).items():
            shared = methods.get("parameters", []) if isinstance(methods, dict) else []
            for http, op in methods.items():
                if http not in HTTP_METHODS or not isinstance(op, dict):
                    continue
                tag = (op.get("tags") or ["default"])[0]
                domain = snake(tag)
                op_id = op.get("operationId")
                if not op_id:
                    synthetic += 1
                    op_id = snake(f"{http}_{path}")
                params = list(shared) + list(op.get("parameters") or [])
                path_params = [p["name"] for p in params if p.get("in") == "path"]
                for token in re.findall(r"\{([^}]+)\}", path):
                    if token not in path_params:
                        path_params.append(token)
                query_params = [p["name"] for p in params if p.get("in") == "query"]
                has_body = "requestBody" in op

                method_name = snake(op_id)
                while method_name in global_methods:
                    method_name += "_x"
                global_methods.add(method_name)

                actions_seen = {o["action"] for o in by_domain.get(domain, [])}
                action = snake(op_id)
                while action in actions_seen:
                    action += "_x"

                summary = (op.get("summary") or op.get("description") or op_id).strip()
                summary = re.sub(r"\s+", " ", summary.splitlines()[0])[:160]

                by_domain.setdefault(domain, []).append(
                    {
                        "operation_id": op_id,
                        "method": method_name,
                        "action": action,
                        "domain": domain,
                        "http": http.upper(),
                        "url_template": base + path,
                        "path_params": path_params,
                        "query_params": query_params,
                        "has_body": has_body,
                        "paginate": detect_pagination(http, query_params),
                        "summary": summary,
                        "params": normalize_params(params, op, spec),
                    }
                )

    print(
        f"Collected {sum(len(v) for v in by_domain.values())} operations "
        f"across {len(by_domain)} domains ({synthetic} synthetic ids)."
    )
    return by_domain


# --------------------------------------------------------------------- emitters
AUTOGEN = (
    '"""Auto-generated by scripts/generate_from_openapi.py — do not edit by hand."""'
)


def emit_client_module(domain: str, ops: list[dict]) -> None:
    cls = f"Gramps{camel(domain)}"
    lines = [
        "#!/usr/bin/python",
        AUTOGEN,
        "",
        "from gramps_mcp.api.api_client_base import GrampsApiBase",
        "from gramps_mcp.gramps_models import Response",
        "",
        "",
        f"class {cls}(GrampsApiBase):",
    ]
    for op in ops:
        doc = op["summary"].replace('"', "'")
        lines += [
            f"    def {op['method']}(self, **kwargs) -> Response:",
            f'        """{doc}"""',
            "        return self._call(",
            f"            http={op['http']!r},",
            f"            url_template={op['url_template']!r},",
            f"            path_params={op['path_params']!r},",
            f"            query_params={op['query_params']!r},",
            f"            has_body={op['has_body']!r},",
            f"            paginate={op['paginate']!r},",
            "            kwargs=kwargs,",
            "        )",
            "",
        ]
    (API_DIR / f"api_client_{domain}.py").write_text("\n".join(lines) + "\n")


def emit_mcp_module(domain: str, ops: list[dict]) -> None:
    tag = domain.replace("_", "-")
    actions = ", ".join(f"'{op['action']}'" for op in ops)
    lines = [
        AUTOGEN,
        "",
        "from typing import Any",
        "",
        "from fastmcp import Context, FastMCP",
        "from fastmcp.dependencies import Depends",
        "from pydantic import Field",
        "",
        "from gramps_mcp.auth import get_client",
        "",
        "",
        f"def register_{domain}_tools(mcp: FastMCP):",
        f'    @mcp.tool(tags={{"{tag}"}})',
        f"    async def gramps_{domain}(",
        "        action: str = Field(",
        f'            description="Action to perform. One of: {actions}"',
        "        ),",
        "        params_json: str = Field(",
        '            default="{}",',
        '            description="JSON string of parameters (path, query, and body '
        'fields) for the action.",',
        "        ),",
        "        client=Depends(get_client),",
        "        ctx: Context | None = Field(",
        '            default=None, description="MCP context for progress reporting"',
        "        ),",
        "    ) -> Any:",
        f'        """Manage Gramps {domain.replace("_", " ")} operations. '
        'CONCEPT:GM-OS.identity.grmp."""',
        "        if ctx:",
        '            await ctx.info(f"Executing gramps_'
        + domain
        + ' action: {action}")',
        "        import json",
        "",
        "        try:",
        "            kwargs = json.loads(params_json) if params_json else {}",
        "        except Exception as e:",
        '            return {"error": f"Invalid params_json: {e}"}',
        "        if not isinstance(kwargs, dict):",
        '            return {"error": "params_json must decode to a JSON object"}',
        "        kwargs = {k: v for k, v in kwargs.items() if v is not None}",
        "",
    ]
    first = True
    for op in ops:
        kw = "if" if first else "elif"
        first = False
        lines.append(f'        {kw} action == "{op["action"]}":')
        lines.append(f"            return client.{op['method']}(**kwargs)")
    lines += [
        '        raise ValueError(f"Unknown action: {action}")',
        "",
    ]
    (MCP_DIR / f"mcp_{domain}.py").write_text("\n".join(lines) + "\n")


def emit_manifest(by_domain: dict[str, list[dict]]) -> None:
    operations = [
        {
            "operation_id": op["operation_id"],
            "domain": domain,
            "method": op["method"],
            "action": op["action"],
            "http": op["http"],
            "path": op["url_template"],
            "paginate": op["paginate"],
            "summary": op["summary"],
            "params": op["params"],
        }
        for domain in sorted(by_domain)
        for op in by_domain[domain]
    ]
    lines = [
        AUTOGEN,
        "",
        "from typing import Any",
        "",
        "# Each entry: {operation_id, domain, method, action, http, path, paginate,",
        "#             summary, params:[{name,type,required,description}]}",
        "# `summary` + `params` drive the verbose 1:1 tool tier "
        "(register_verbose_tools).",
        f"OPERATIONS: list[dict[str, Any]] = {operations!r}",
        "",
        "DOMAINS = " + json.dumps(sorted(by_domain), indent=4),
        "",
        "# domain -> ordered list of MCP action names",
        "ACTIONS_BY_DOMAIN: dict[str, list[str]] = {}",
        "for _op in OPERATIONS:",
        "    ACTIONS_BY_DOMAIN.setdefault(_op['domain'], []).append(_op['action'])",
        "",
    ]
    (API_DIR / "_operation_manifest.py").write_text("\n".join(lines) + "\n")


def emit_api_client(by_domain: dict[str, list[dict]]) -> None:
    domains = sorted(by_domain)
    imports = [
        f"from gramps_mcp.api.api_client_{d} import Gramps{camel(d)}"
        for d in domains
    ]
    bases = ",\n    ".join(f"Gramps{camel(d)}" for d in domains)
    lines = [
        "#!/usr/bin/python",
        AUTOGEN,
        "",
        *imports,
        "",
        "",
        f"class Api(\n    {bases},\n):",
        '    """Composite Gramps API client — every domain client, one class."""',
        "",
        "    __slots__ = ()",
        "",
    ]
    (PKG / "api_client.py").write_text("\n".join(lines) + "\n")


def emit_mcp_init(by_domain: dict[str, list[dict]]) -> None:
    domains = sorted(by_domain)
    imports = [
        f"from gramps_mcp.mcp.mcp_{d} import register_{d}_tools" for d in domains
    ]
    registry = [f'    ("{d}", "{d.upper()}TOOL", register_{d}_tools),' for d in domains]
    lines = [
        AUTOGEN,
        "",
        *imports,
        "",
        "# (tag, toggle_env_var, register_fn) — consumed by "
        "mcp_server.get_mcp_instance().",
        "TOOL_REGISTRY = [",
        *registry,
        "]",
        "",
        "__all__ = [",
        *[f'    "register_{d}_tools",' for d in domains],
        '    "TOOL_REGISTRY",',
        "]",
        "",
    ]
    (MCP_DIR / "__init__.py").write_text("\n".join(lines) + "\n")


def main() -> None:
    API_DIR.mkdir(exist_ok=True)
    MCP_DIR.mkdir(exist_ok=True)
    by_domain = collect_operations()
    for domain, ops in by_domain.items():
        emit_client_module(domain, ops)
        emit_mcp_module(domain, ops)
    emit_manifest(by_domain)
    emit_api_client(by_domain)
    emit_mcp_init(by_domain)
    # Reflow the emitted code to satisfy the ruff-format pre-commit gate so that
    # re-running the generator is idempotent under the project's quality bar.
    import shutil
    import subprocess

    ruff = shutil.which("ruff")
    if ruff:
        targets = [str(API_DIR), str(MCP_DIR), str(PKG / "api_client.py")]
        subprocess.run([ruff, "check", "--fix", "--quiet", *targets], check=False)
        subprocess.run([ruff, "format", "--quiet", *targets], check=False)
    print(f"Generated {len(by_domain)} client modules + MCP tools.")


if __name__ == "__main__":
    main()
