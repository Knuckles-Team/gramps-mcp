#!/usr/bin/env python3
"""Run a bounded, content-free A2A readiness probe against a runtime URL."""

from __future__ import annotations

import argparse
import asyncio
import uuid
from urllib.parse import urlsplit

import httpx
from agent_utilities.core.transport_security import resolve_configured_tls_profile


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Runtime A2A endpoint")
    return parser


async def _probe(url: str) -> int:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        print("A2A readiness failed (invalid HTTPS URL)")
        return 1
    if parsed.username or parsed.password or parsed.fragment:
        print("A2A readiness failed (invalid URL authority)")
        return 1
    profile = resolve_configured_tls_profile("gramps_a2a")
    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "kind": "message",
                "role": "user",
                "parts": [{"kind": "text", "text": "Return readiness status only."}],
                "messageId": str(uuid.uuid4()),
            }
        },
        "id": 1,
    }
    try:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=False,
            **profile.httpx_kwargs(),
        ) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            decoded = response.json()
            if not isinstance(decoded, dict) or (
                "result" not in decoded and "error" not in decoded
            ):
                raise RuntimeError("A2A response had an invalid shape")
    except Exception as exc:
        print(f"A2A readiness failed ({type(exc).__name__})")
        return 1
    finally:
        profile.cleanup()
    print("A2A readiness succeeded")
    return 0


def main() -> int:
    args = _parser().parse_args()
    return asyncio.run(_probe(args.url))


if __name__ == "__main__":
    raise SystemExit(main())
