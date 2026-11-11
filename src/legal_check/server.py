"""Legal Check MCP server.

Run locally (stdio):   uv run legal-check
Run over HTTP:          uv run legal-check --transport streamable-http --port 8000

Privacy (brief D6, D16): tools take only facts and country codes, never the
user's idea text or code. Nothing is stored. Logs hold counts and errors only.
"""

from __future__ import annotations

import argparse
import logging
from typing import Annotated, Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from . import __version__
from .checker import FactError, build_facts, check
from .library import Library, LibraryError, load_library

log = logging.getLogger("legal_check")
# Store nothing (brief D6): the MCP library logs tool error messages at INFO, and
# those can contain the user's input. Keep only its warnings and errors.
# tests/test_server.py::test_logs_never_contain_user_input checks this.
logging.getLogger("mcp").setLevel(logging.WARNING)

INSTRUCTIONS = """\
Legal Check spots legal issues for software products, starting with Sri Lankan law.
It gives legal information, not legal advice.

When the user plans or builds a feature for a product with users in Sri Lanka, or
made by a Sri Lankan company or person:
1. If you don't know yet, ask where the users are, where the company is, and what
   personal data is collected.
2. Call get_fact_questions once to learn the facts you may send.
3. Call check_legal_risks with the facts that are true for the feature. Send only
   facts and country codes, never the user's idea text or code.
4. Explain only what the tool returns, Must items first, with the law and section.
   Never add laws of your own, and never say the product is "compliant" or
   "all clear": say "no issues found in the areas we cover" and list what isn't covered.
5. If the user says a warning is already handled, pass its rule_id in `done` on
   later checks. Done items are listed separately, not verified: remind the user
   to check them. Never mark something done unless the user said so.
6. Say that draft rules are not yet reviewed by a lawyer. If the tool returns an
   error, tell the user the check failed; do not treat it as "no issues".
7. If the user asks how to avoid or get around a law, explain the law and the
   risk instead of helping to evade it.
"""

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False, idempotentHint=True)

_library: Library | None = None
_load_error: str | None = None


def _get_library() -> Library:
    if _library is None:
        raise ToolError(
            f"Legal Check could not load its rule library ({_load_error}). "
            "The check did NOT run: this is not a 'no issues found' result."
        )
    return _library


def load(rules_dir=None) -> None:
    global _library, _load_error
    try:
        _library = load_library(rules_dir)
        _load_error = None
        log.info("rule library loaded: %d rules", len(_library.rules))
    except LibraryError as exc:
        _library, _load_error = None, str(exc)
        log.error("rule library failed to load: %s", exc)


mcp = MCPServer(
    name="legal-check",
    title="Legal Check",
    instructions=INSTRUCTIONS,
    version=__version__,
)


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "Check a planned or new feature for legal risks. Call this whenever the user plans "
        "or builds a feature for a product used in Sri Lanka, or made by a Sri Lankan "
        "company or person, even if they didn't ask about law. Send country codes and "
        "facts from get_fact_questions only (no idea text, no code). Returns warnings "
        "with severity (Must / Should / Check with a lawyer), the law and section, what "
        "to do, and the areas NOT covered."
    ),
)
def check_legal_risks(
    users_in: Annotated[
        list[str], Field(description="ISO country codes where users are, e.g. ['LK']")
    ],
    facts: Annotated[list[str], Field(description="Facts that are true, from get_fact_questions")],
    company_in: Annotated[
        str | None, Field(description="ISO country code where the company (or maker) is")
    ] = None,
    processing_in: Annotated[
        list[str] | None, Field(description="ISO country codes where data is stored or processed")
    ] = None,
    done: Annotated[
        list[str] | None,
        Field(
            description="rule_id values of warnings the user says are already handled. "
            "Only when the user says so; they are listed as 'done', not verified."
        ),
    ] = None,
) -> dict[str, Any]:
    library = _get_library()
    all_facts = build_facts(users_in, facts, company_in, processing_in)
    try:
        result = check(library, all_facts, set(done or []))
    except FactError as exc:
        log.info("check rejected: %d unknown fact(s)", str(exc).count("'") // 2)
        raise ToolError(str(exc)) from exc
    log.info("check: %d facts, %d warnings", len(all_facts), len(result["warnings"]))
    return result


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "List the facts check_legal_risks understands, grouped, each with the question "
        "it answers. Call once before check_legal_risks."
    ),
)
def get_fact_questions() -> dict[str, Any]:
    library = _get_library()
    return {
        "country_facts": "Pass countries as users_in, company_in, processing_in (ISO codes).",
        "facts": {k: v for k, v in library.questions.items() if k != "where"},
    }


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "Get one rule in full, including the exact quote from the law and its official "
        "source link. Use it to show proof for a warning."
    ),
)
def get_rule(
    rule_id: Annotated[str, Field(description="rule_id from a check_legal_risks warning")],
) -> dict[str, Any]:
    library = _get_library()
    rule = library.rules.get(rule_id)
    if rule is None:
        raise ToolError(f"No rule with id {rule_id!r}.")
    return {
        **{k: rule[k] for k in ("id", "title", "severity", "area", "why", "what_to_do")},
        "law": rule["law"],
        "in_force": rule["in_force"],
        "starts_on": str(rule["starts_on"]) if rule["starts_on"] else None,
        "last_checked": str(rule["last_checked"]),
        "review_status": rule["review_status"],
        "notes": rule.get("notes", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(prog="legal-check", description=__doc__.split("\n")[0])
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    # stderr only: stdout is the MCP channel in stdio mode.
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    load()
    if args.transport == "stdio":
        mcp.run("stdio")
    else:
        mcp.run("streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
