"""Usage counts: one log line per tool call, numbers and fixed words only.

    usage tool=check_legal_risks client=claude-code result=ok facts=5 warnings=8 must=3
          client_duties=0 done=0 areas=personal-data,telecom covered=yes   (one line)

Store nothing (brief D6): never facts, country codes, rule ids, idea text, code or IP
addresses. `client` is the AI tool's name from MCP (mapped to a short fixed list), `areas`
are rule area names from rules/<area>/. scripts/usage.py reads these lines back from the
Azure log and prints the totals. tests/test_server.py checks no user input gets in.
"""

from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("legal_check")

# Substring of the MCP client name (or User-Agent) -> short name. First match wins.
CLIENTS = [
    ("claude-code", "claude-code"),
    ("claude", "claude"),
    ("codex", "codex"),
    ("cursor", "cursor"),
    ("visual studio code", "vscode"),
    ("vscode", "vscode"),
    ("copilot", "vscode"),
    ("windsurf", "windsurf"),
    ("gemini", "gemini"),
    ("chatgpt", "chatgpt"),
    ("openai", "chatgpt"),
]


def client_name(ctx: Any) -> str:
    """The AI tool calling us, as one word from CLIENTS, 'other' or 'unknown'.
    Never the raw name, so nothing a client sends can reach the log as free text."""
    raw = ""
    try:
        rc = ctx.request_context
        params = rc.session.client_params
        if params is not None:
            raw = params.client_info.name or ""
        if not raw and rc.request is not None:
            raw = rc.request.headers.get("user-agent", "")
    except Exception:  # no request (tests calling the function directly)
        return "unknown"
    raw = raw.lower()
    if not raw:
        return "unknown"
    return next((short for key, short in CLIENTS if key in raw), "other")


def record(tool: str, ctx: Any, result: str = "ok", **counts: Any) -> None:
    """Log one usage line. `counts` values must be numbers, or fixed words we choose."""
    parts = [f"tool={tool}", f"client={client_name(ctx)}", f"result={result}"]
    parts += [f"{k}={v}" for k, v in counts.items()]
    log.info("usage %s", " ".join(parts))


def check_counts(result: dict[str, Any]) -> dict[str, Any]:
    """Counts for a check_legal_risks result: warnings, Must items, matched areas."""
    client = (result.get("client_duties") or {}).get("items", [])
    areas = sorted({w["area"] for w in result["warnings"]})
    return {
        "warnings": len(result["warnings"]),
        "must": sum(w["severity"] == "Must" for w in result["warnings"]),
        "client_duties": len(client),
        "done": len(result["done"]),
        "areas": ",".join(areas) or "none",
        "covered": "no" if _no_country_covered(result) else "yes",
    }


def _no_country_covered(result: dict[str, Any]) -> bool:
    return "None of the given countries are covered" in result["summary"]
