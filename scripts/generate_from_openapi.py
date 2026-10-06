#!/usr/bin/env python
"""Generate the Gramps API client + MCP tools from the vendored OpenAPI spec.

This is an **author-time** developer tool, not a runtime dependency. It reads the
spec(s) in ``gramps_mcp/specs/*.json`` and emits fleet-conformant, committed
code:

* ``gramps_mcp/api/api_client_<domain>.py`` — one method per OpenAPI operation,
  composed into ``gramps_mcp.api.Api`` via multiple inheritance.
* ``gramps_mcp/api/_operation_manifest.py`` — the machine-readable
  ``operationId → method → action`` map that the coverage test asserts against and
  that drives the verbose 1:1 tool tier.
* ``gramps_mcp/mcp/mcp_<domain>.py`` — one consolidated, action-routed MCP tool
  per domain exposing every operation as an ``action``.
* ``gramps_mcp/mcp/__init__.py`` — ``TOOL_REGISTRY`` consumed by ``mcp_server.py``.
* ``gramps_mcp/api/__init__.py`` — the composite ``Api`` class.

The OpenAPI spec is derived from the documented Gramps REST routes
(``gramps-project/gramps-web-api``) — see ``gramps_mcp/specs/``.

After refreshing the specs, run the read-only reconciler:
``python scripts/generate_from_openapi.py``. Use ``--apply`` only for additive
operations; ``--scaffold`` is reserved for a brand-new repository and refuses
to overwrite an existing MCP module.
"""

from __future__ import annotations

import argparse
import ast
import json
import keyword
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

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
    """Return only the deployment-neutral path prefix from the first server."""
    servers = spec.get("servers") or [{}]
    return urlsplit(servers[0].get("url", "")).path.rstrip("/")


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


def _param_entries_from_list(params: list, spec: dict, seen: set[str]) -> list[dict]:
    """Flatten declared path/query parameters into typed entries, deduped by name."""
    out: list[dict] = []
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
    return out


def _request_body_schema(spec: dict, op: dict) -> tuple[dict, dict] | None:
    """Return ``(request_body, resolved_media_schema)``, or ``None`` when there is no body."""
    request_body = _resolve_ref(spec, op.get("requestBody") or {})
    if not request_body:
        return None
    content = request_body.get("content") or {}
    media: dict = content.get("application/json") or next(iter(content.values()), {})
    schema = _resolve_ref(spec, (media or {}).get("schema") or {})
    return request_body, schema


def _param_entries_from_body(spec: dict, op: dict, seen: set[str]) -> list[dict]:
    """Flatten top-level requestBody fields into typed entries, deduped by name."""
    resolved = _request_body_schema(spec, op)
    if resolved is None:
        return []
    request_body, schema = resolved
    props = schema.get("properties") or {}
    if not props:
        return [
            {
                "name": "body",
                "type": "object",
                "required": bool(request_body.get("required")),
                "description": "Request body (JSON object).",
            }
        ]
    required = set(schema.get("required") or [])
    out: list[dict] = []
    for pname, pschema in props.items():
        if pname in seen:
            continue
        seen.add(pname)
        ps = _resolve_ref(spec, pschema)
        out.append(_param_entry(pname, ps, pname in required, ps.get("description")))
    return out


def normalize_params(params: list, op: dict, spec: dict) -> list[dict]:
    """Flatten path/query params + top-level requestBody fields into typed entries."""
    seen: set[str] = set()
    out = _param_entries_from_list(params, spec, seen)
    out.extend(_param_entries_from_body(spec, op, seen))
    return out


@dataclass
class _SpecContext:
    """The per-spec-file context an operation is built against."""

    spec: dict
    base: str
    shared: list


@dataclass
class _OperationRegistry:
    """Cross-domain method-name and per-domain action-name dedup state."""

    global_methods: set[str] = field(default_factory=set)
    domain_actions: dict[str, set[str]] = field(default_factory=dict)

    def unique_method(self, candidate: str) -> str:
        while candidate in self.global_methods:
            candidate += "_x"
        self.global_methods.add(candidate)
        return candidate

    def unique_action(self, domain: str, candidate: str) -> str:
        seen = self.domain_actions.setdefault(domain, set())
        while candidate in seen:
            candidate += "_x"
        seen.add(candidate)
        return candidate


def _iter_path_operations(methods: dict):
    """Yield the real HTTP-method ``(http, op)`` pairs for one path item."""
    for http, op in methods.items():
        if http not in HTTP_METHODS or not isinstance(op, dict):
            continue
        yield http, op


def _operation_path_params(params: list, path: str) -> list[str]:
    path_params = [p["name"] for p in params if p.get("in") == "path"]
    for token in re.findall(r"\{([^}]+)\}", path):
        if token not in path_params:
            path_params.append(token)
    return path_params


def _operation_entry(
    http: str,
    op: dict,
    path: str,
    ctx: _SpecContext,
    registry: _OperationRegistry,
) -> tuple[str, dict, bool]:
    """Build one operation_meta dict; returns ``(domain, entry, was_synthetic_id)``."""
    tag = (op.get("tags") or ["default"])[0]
    domain = snake(tag)
    op_id = op.get("operationId")
    synthetic = not op_id
    if not op_id:
        op_id = snake(f"{http}_{path}")
    params = list(ctx.shared) + list(op.get("parameters") or [])
    path_params = _operation_path_params(params, path)
    query_params = [p["name"] for p in params if p.get("in") == "query"]
    has_body = "requestBody" in op

    method_name = registry.unique_method(snake(op_id))
    action = registry.unique_action(domain, snake(op_id))

    summary = (op.get("summary") or op.get("description") or op_id).strip()
    summary = re.sub(r"\s+", " ", summary.splitlines()[0])[:160]

    entry = {
        "operation_id": op_id,
        "method": method_name,
        "action": action,
        "domain": domain,
        "http": http.upper(),
        "url_template": ctx.base + path,
        "path_params": path_params,
        "query_params": query_params,
        "has_body": has_body,
        "paginate": detect_pagination(http, query_params),
        "summary": summary,
        "params": normalize_params(params, op, ctx.spec),
    }
    return domain, entry, synthetic


def collect_operations() -> dict[str, list[dict]]:
    """Return ``{domain: [operation_meta, ...]}`` across all vendored specs."""
    by_domain: dict[str, list[dict]] = {}
    registry = _OperationRegistry()
    synthetic = 0

    for spec_path in sorted(SPECS_DIR.glob("*.json")):
        spec = json.loads(spec_path.read_text())
        ctx_base = server_template(spec)

        for path, methods in (spec.get("paths") or {}).items():
            shared = methods.get("parameters", []) if isinstance(methods, dict) else []
            ctx = _SpecContext(spec=spec, base=ctx_base, shared=shared)
            for http, op in _iter_path_operations(methods):
                domain, entry, was_synthetic = _operation_entry(
                    http, op, path, ctx, registry
                )
                synthetic += was_synthetic
                by_domain.setdefault(domain, []).append(entry)

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
        "import json",
        "",
        "from typing import Any",
        "",
        "from agent_utilities.mcp.action_dispatch import resolve_action",
        "from agent_utilities.mcp.concurrency import run_blocking",
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
        f'            await ctx.info("Executing Gramps {domain.replace("_", " ")} operation")',
        "",
        '        if len(params_json.encode("utf-8")) > 1_048_576:',
        '            return {"error": "params_json exceeds the connector limit"}',
        "        try:",
        "            kwargs = json.loads(params_json) if params_json else {}",
        "        except (TypeError, ValueError):",
        '            return {"error": "Invalid params_json"}',
        "        if not isinstance(kwargs, dict):",
        '            return {"error": "params_json must decode to a JSON object"}',
        "        kwargs = {k: v for k, v in kwargs.items() if v is not None}",
        "        resolved = resolve_action(",
        "            action,",
        "            {",
        *[f'                "{op["action"]}",' for op in ops],
        "            },",
        '            service="gramps",',
        "        )",
        "        if isinstance(resolved, dict):",
        "            return resolved",
        "        method = getattr(client, resolved, None)",
        "        if method is None:",
        '            return {"error": "Unknown action"}',
        "        return await run_blocking(method, **kwargs)",
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
        f"from gramps_mcp.api.api_client_{d} import Gramps{camel(d)}" for d in domains
    ]
    bases = ",\n    ".join(f"Gramps{camel(d)}" for d in domains)
    lines = [
        AUTOGEN,
        "",
        *imports,
        "from gramps_mcp.api.api_client_base import GrampsApiBase",
        "",
        "",
        f"class Api(\n    {bases},\n):",
        '    """Composite Gramps API client — every domain client, one class."""',
        "",
        "    __slots__ = ()",
        "",
        '__all__ = ["Api", "GrampsApiBase"]',
        "",
    ]
    (API_DIR / "__init__.py").write_text("\n".join(lines) + "\n")


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


# --------------------------------------------------------------- reconciler
#
# Regenerating whole files on every run is the defect this reconciler exists
# to remove: it would silently overwrite hand-maintained code. So the default
# mode of this script is now READ-ONLY reconciliation -- it diffs the
# vendored spec(s) against the committed source and reports drift, never
# writes. ``--scaffold`` is the old full-generation behavior, kept only for a
# brand-new repo with no MCP module yet (it refuses to touch anything that
# already exists). ``--apply`` inserts ONLY the additive delta (new handlers
# for actions the spec added) in the exact shape the file already uses --
# gramps routes through ``resolve_action(action, {<action set>}, ...)``
# rather than an elif chain, so "the shape" here means splicing new string
# literals into that set -- and never touches an existing line; renames,
# signature changes, and removals are reported for a human, never
# auto-applied.


class Finding:
    __slots__ = ("kind", "domain", "action", "detail")

    def __init__(self, kind: str, domain: str, detail: str, action: str | None = None):
        self.kind = kind
        self.domain = domain
        self.action = action
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.kind}] {self.domain}: {self.detail}"


def _extract_handled_actions(src: str) -> set[str]:
    """Extract the set of action strings a gramps mcp_<domain>.py module
    routes, by finding the ``resolve_action(action, {...}, service=...)``
    call and reading the string constants out of its set-literal second
    argument via ``ast`` -- not by re-deriving it, so a hand-edited set still
    reconciles honestly against what the code actually does.
    """
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "resolve_action"
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Set)
        ):
            return {
                elt.value
                for elt in node.args[1].elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            }
    return set()


def _extract_client_methods(src: str) -> set[str]:
    """Return public methods declared by a generated domain client module."""
    methods: set[str] = set()
    tree = ast.parse(src)
    for class_node in tree.body:
        if not isinstance(class_node, ast.ClassDef):
            continue
        methods.update(
            node.name
            for node in class_node.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
        )
    return methods


def _existing_mcp_domains() -> set[str]:
    """Return every domain module, including hand-maintained files.

    The autogenerated marker identifies files emitted by this script, but it
    is not an ownership marker. Reconciliation must never mistake a manually
    maintained module for a missing domain, and scaffold must refuse to write
    over it.
    """
    return {
        p.stem[len("mcp_") :]
        for p in MCP_DIR.glob("mcp_*.py")
        if p.stem not in ("mcp_custom_api", "__init__")
    }


def _find_call_node(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
) -> ast.Call | None:
    """Find the ``self._call(...)`` call inside one method body, if any."""
    for n in ast.walk(func):
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "_call"
        ):
            return n
    return None


def _signature_from_call(call: ast.Call) -> tuple | None:
    """Read a ``self._call(...)``'s literal keyword arguments into a signature tuple."""
    kwargs = {kw.arg: kw.value for kw in call.keywords if kw.arg}
    try:
        http = ast.literal_eval(kwargs["http"])
        url_template = ast.literal_eval(kwargs["url_template"])
        path_params = tuple(ast.literal_eval(kwargs["path_params"]))
        query_params = tuple(sorted(ast.literal_eval(kwargs["query_params"])))
        has_body = ast.literal_eval(kwargs["has_body"])
        paginate = ast.literal_eval(kwargs["paginate"])
    except (KeyError, TypeError, ValueError):
        return None
    return (http, url_template, path_params, query_params, has_body, paginate)


def _extract_client_signatures(src: str) -> dict[str, tuple]:
    """Parse an ``api_client_<domain>.py`` module and return
    ``{method_name: (http, url_template, path_params, query_params, has_body, paginate)}``
    by reading each method's ``self._call(...)`` keyword arguments via ``ast``.
    """
    sigs: dict[str, tuple] = {}
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        call = _find_call_node(node)
        if call is None:
            continue
        signature = _signature_from_call(call)
        if signature is not None:
            sigs[node.name] = signature
    return sigs


def _op_signature(op: dict) -> tuple:
    return (
        op["http"],
        op["url_template"],
        tuple(op["path_params"]),
        tuple(sorted(op["query_params"])),
        op["has_body"],
        op["paginate"],
    )


def _new_domain_findings(spec_domains: set[str], existing: set[str], by_domain: dict) -> list[Finding]:
    return [
        Finding(
            "NEW DOMAIN",
            domain,
            f"{len(by_domain[domain])} action(s) in the spec, no mcp_{domain}.py "
            f"yet -- scaffold is for a brand-new repo only "
            f"(refuses if any mcp_*.py already exists); hand-author this domain's "
            f"file once, then reconcile/--apply will track it going forward.",
        )
        for domain in sorted(spec_domains - existing)
    ]


def _orphaned_domain_findings(spec_domains: set[str], existing: set[str]) -> list[Finding]:
    return [
        Finding(
            "ORPHANED DOMAIN",
            domain,
            f"mcp_{domain}.py exists but the domain no longer appears in the "
            f"spec(s) at all -- likely dropped upstream. Not auto-removed.",
        )
        for domain in sorted(existing - spec_domains)
    ]


def _handler_findings(domain: str, spec_actions: dict, handled: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for action in sorted(set(spec_actions) - handled):
        op = spec_actions[action]
        findings.append(
            Finding(
                "MISSING HANDLER",
                domain,
                f"action '{action}' ({op['operation_id']}) is in the spec but "
                f"resolve_action()'s set in mcp_{domain}.py doesn't route it.",
                action=action,
            )
        )
    for action in sorted(handled - set(spec_actions)):
        findings.append(
            Finding(
                "ORPHANED HANDLER",
                domain,
                f"mcp_{domain}.py routes action '{action}' but the spec no longer "
                f"has a matching operation -- likely renamed or removed upstream.",
                action=action,
            )
        )
    return findings


def _signature_drift_findings(domain: str, spec_actions: dict, handled: set[str]) -> list[Finding]:
    """Report missing clients and request/pagination signature changes."""
    client_path = API_DIR / f"api_client_{domain}.py"
    if not client_path.exists():
        return [
            Finding(
                "MISSING CLIENT MODULE",
                domain,
                f"mcp_{domain}.py exists, but api_client_{domain}.py is absent; "
                "the routed actions cannot reach an API client.",
            )
        ]
    client_src = client_path.read_text()
    client_methods = _extract_client_methods(client_src)
    client_sigs = _extract_client_signatures(client_src)
    findings: list[Finding] = []
    for action in sorted(set(spec_actions) & handled):
        op = spec_actions[action]
        method = op["method"]
        if method not in client_methods:
            findings.append(
                Finding(
                    "MISSING CLIENT METHOD",
                    domain,
                    f"action '{action}' routes in mcp_{domain}.py but its "
                    f"expected client method {method} is absent from "
                    f"api_client_{domain}.py.",
                    action=action,
                )
            )
            continue
        if method not in client_sigs:
            findings.append(
                Finding(
                    "UNREADABLE CLIENT SIGNATURE",
                    domain,
                    f"action '{action}' routes to client.{method}, but its "
                    "self._call signature is not statically readable; "
                    "manual review is required before claiming parity.",
                    action=action,
                )
            )
            continue
        if client_sigs[method] != _op_signature(op):
            findings.append(
                Finding(
                    "SIGNATURE DRIFT",
                    domain,
                    f"operation '{op['operation_id']}' (method {method}) "
                    f"parameters changed: code has {client_sigs[method]}, spec "
                    f"now has {_op_signature(op)}.",
                    action=action,
                )
            )
    return findings


def _domain_findings(domain: str, ops: list[dict]) -> list[Finding]:
    spec_actions = {op["action"]: op for op in ops}
    mcp_path = MCP_DIR / f"mcp_{domain}.py"
    handled = _extract_handled_actions(mcp_path.read_text())
    findings = _handler_findings(domain, spec_actions, handled)
    findings += _signature_drift_findings(domain, spec_actions, handled)
    return findings


def reconcile(by_domain: dict[str, list[dict]]) -> list[Finding]:
    """Compare the current spec(s) against the existing hand-maintained
    source. Read-only -- never writes anything.
    """
    existing_mcp_domains = _existing_mcp_domains()
    spec_domains = set(by_domain)

    findings: list[Finding] = []
    findings += _new_domain_findings(spec_domains, existing_mcp_domains, by_domain)
    findings += _orphaned_domain_findings(spec_domains, existing_mcp_domains)
    for domain in sorted(spec_domains & existing_mcp_domains):
        findings += _domain_findings(domain, by_domain[domain])
    return findings


def print_report(findings: list[Finding]) -> None:
    if not findings:
        print(
            "reconcile: OK -- no drift between the vendored spec(s) and the "
            "committed source."
        )
        return
    by_kind: dict[str, int] = {}
    for f in findings:
        by_kind[f.kind] = by_kind.get(f.kind, 0) + 1
        print(str(f))
    print()
    print(
        "reconcile: DRIFT FOUND -- "
        + ", ".join(f"{n} {k}" for k, n in sorted(by_kind.items()))
    )


def scaffold(by_domain: dict[str, list[dict]]) -> None:
    """One-time bootstrap for a brand-new repo with no MCP module yet.

    Refuses outright if any mcp_<domain>.py already exists -- scaffold never
    overwrites hand-maintained code. Use the default reconcile mode (or
    --apply) on an established repo instead.
    """
    API_DIR.mkdir(exist_ok=True)
    MCP_DIR.mkdir(exist_ok=True)
    existing = [
        p
        for p in MCP_DIR.glob("mcp_*.py")
        if p.stem != "__init__"
    ]
    if existing:
        print(
            f"scaffold: refusing -- {len(existing)} mcp_*.py file(s) already exist "
            f"({', '.join(sorted(p.name for p in existing))}). scaffold is for a "
            f"brand-new repo only; use the default reconcile mode (or --apply) "
            f"instead."
        )
        raise SystemExit(1)
    for domain, ops in by_domain.items():
        emit_client_module(domain, ops)
        emit_mcp_module(domain, ops)
    emit_manifest(by_domain)
    emit_api_client(by_domain)
    emit_mcp_init(by_domain)
    import shutil
    import subprocess

    ruff = shutil.which("ruff")
    if ruff:
        targets = [str(API_DIR), str(MCP_DIR)]
        subprocess.run([ruff, "check", "--fix", "--quiet", *targets], check=False)
        subprocess.run([ruff, "format", "--quiet", *targets], check=False)
    print(f"scaffold: generated {len(by_domain)} client modules + MCP tools.")


def _render_client_insertion(op: dict) -> list[str]:
    doc = op["summary"].replace('"', "'")
    return [
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


def _append_client_methods(client_path: Path, new_ops: list[dict]) -> None:
    """Append new methods at the end of an ``api_client_<domain>.py`` class."""
    client_lines = client_path.read_text().splitlines()
    insertion: list[str] = []
    for op in new_ops:
        insertion += _render_client_insertion(op)
    while client_lines and client_lines[-1] == "":
        client_lines.pop()
    client_lines += [""] + insertion
    client_path.write_text("\n".join(client_lines) + "\n")


def _splice_action_strings(mcp_lines: list[str], new_ops: list[dict]) -> list[str]:
    """Splice new action string literals into the ``resolve_action(...)`` set,
    right before its closing ``},``.
    """
    open_idx = next(i for i, line in enumerate(mcp_lines) if line.strip() == "{")
    close_idx = next(
        i for i in range(open_idx + 1, len(mcp_lines)) if mcp_lines[i].strip() == "},"
    )
    new_set_lines = [f'                "{op["action"]}",' for op in new_ops]
    return mcp_lines[:close_idx] + new_set_lines + mcp_lines[close_idx:]


def _appended_description_line(line: str, new_ops: list[dict]) -> str:
    """Append any not-yet-listed action onto one "Action to perform. One of:
    ..." Field description line, before its closing quote.
    """
    already_listed = set(re.findall(r"'([^']+)'", line))
    still_new = [op for op in new_ops if op["action"] not in already_listed]
    if not still_new:
        return line
    added = ", ".join(f"'{op['action']}'" for op in still_new)
    return line.rstrip()[:-1] + f', {added}"'


def _sync_action_description(mcp_lines: list[str], new_ops: list[dict]) -> list[str]:
    """Keep the "Action to perform. One of: ..." Field description in sync --
    purely additive text appended before the closing quote, skipping any
    action the description already lists.
    """
    for i, line in enumerate(mcp_lines):
        if 'description="Action to perform. One of:' in line:
            mcp_lines[i] = _appended_description_line(line, new_ops)
            break
    return mcp_lines


def _apply_mcp_module(mcp_path: Path, new_ops: list[dict]) -> None:
    mcp_lines = mcp_path.read_text().splitlines()
    mcp_lines = _splice_action_strings(mcp_lines, new_ops)
    mcp_lines = _sync_action_description(mcp_lines, new_ops)
    mcp_path.write_text("\n".join(mcp_lines) + "\n")


def _apply_domain(domain: str, ops: list[dict], missing_actions: set[str]) -> bool:
    """Additively insert handlers for ``missing_actions`` into
    ``mcp_<domain>.py`` (splice new string literals into the
    ``resolve_action(...)`` set) and ``api_client_<domain>.py`` (append new
    methods at the end of the class). Never rewrites, reorders, or deletes an
    existing line. Returns True if anything changed.
    """
    mcp_path = MCP_DIR / f"mcp_{domain}.py"
    client_path = API_DIR / f"api_client_{domain}.py"
    if not mcp_path.exists() or not client_path.exists():
        return False

    ops_by_action = {op["action"]: op for op in ops}
    new_ops = [ops_by_action[a] for a in sorted(missing_actions) if a in ops_by_action]
    if not new_ops:
        return False

    _append_client_methods(client_path, new_ops)
    _apply_mcp_module(mcp_path, new_ops)
    return True


def _missing_handlers_by_domain(findings: list[Finding]) -> dict[str, set[str]]:
    missing_by_domain: dict[str, set[str]] = {}
    for f in findings:
        if f.kind == "MISSING HANDLER" and f.action is not None:
            missing_by_domain.setdefault(f.domain, set()).add(f.action)
    return missing_by_domain


def _apply_missing_handlers(
    by_domain: dict[str, list[dict]], findings: list[Finding]
) -> list[Finding]:
    """Insert every missing handler additively, then re-run reconcile fresh."""
    missing_by_domain = _missing_handlers_by_domain(findings)
    changed_any = False
    for domain, actions in missing_by_domain.items():
        if _apply_domain(domain, by_domain[domain], actions):
            changed_any = True
            print(f"apply: inserted {len(actions)} handler(s) into domain '{domain}'.")
    if changed_any:
        emit_manifest(by_domain)
        print("apply: regenerated _operation_manifest.py (pure derived data).")
    return reconcile(by_domain)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile (default, read-only) the vendored OpenAPI spec(s) against "
            "the committed, hand-maintained MCP source; --scaffold bootstraps a "
            "brand-new repo once; --apply additively inserts new handlers only."
        )
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="One-time bootstrap for a brand-new repo with no MCP module yet. "
        "Refuses to touch anything that already exists.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Additively insert handlers for actions the spec has but the code "
        "doesn't. Never touches an existing line; renames, signature changes, "
        "and removals are reported for a human, never auto-applied.",
    )
    args = parser.parse_args()

    by_domain = collect_operations()

    if args.scaffold:
        scaffold(by_domain)
        return

    findings = reconcile(by_domain)
    if args.apply:
        findings = _apply_missing_handlers(by_domain, findings)

    print_report(findings)
    if findings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
