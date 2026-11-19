"""Rulewise MCP server.

Run locally (stdio):   uv run legal-check
Run over HTTP:          uv run legal-check --transport streamable-http --port 8000

Privacy (brief D6, D16): tools take only facts and country codes, never the
user's idea text or code. Nothing is stored. Logs hold counts and errors only.
"""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Annotated, Any

from mcp.server.mcpserver import Context, MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from . import __version__, usage
from .checker import FactError, build_facts, check, checklist, fact_list
from .library import Library, LibraryError, load_library

log = logging.getLogger("legal_check")
# Store nothing (brief D6): the MCP library logs tool error messages at INFO, and
# those can contain the user's input. Keep only its warnings and errors.
# tests/test_server.py::test_logs_never_contain_user_input checks this.
logging.getLogger("mcp").setLevel(logging.WARNING)

INSTRUCTIONS = """\
Rulewise spots legal issues for software products, starting with Sri Lankan law.
It gives legal information, not legal advice.

When the user plans or builds a product or feature (an app, website or online service):
1. Where are the users and the company? Never guess the country.
   - If the user already said (for example "for Sri Lanka"), go on.
   - If not, ask one short question before checking, for example: "Rulewise checks
     Sri Lankan law. Will your users or your company be in Sri Lanka?"
   - If neither is in Sri Lanka, say Rulewise does not cover that country yet (no
     check, and never "no issues").
   If you don't know yet, also ask what personal data is collected.
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
   End with the result's `feedback` line once (where to report a wrong or missed law).
7. If the user asks how to avoid or get around a law, explain the law and the
   risk instead of helping to evade it.
"""

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False, idempotentHint=True)

_library: Library | None = None
_load_error: str | None = None


def _get_library(tool: str, ctx: Context | None = None) -> Library:
    if _library is None:
        usage.record(tool, ctx, "error", reason="library")
        raise ToolError(
            f"Rulewise could not load its rule library ({_load_error}). "
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
    name="rulewise",
    title="Rulewise",
    instructions=INSTRUCTIONS,
    version=__version__,
)


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "Check a planned or new feature for legal risks. Call this whenever the user plans "
        "or builds a feature for a product used in Sri Lanka, or made by a Sri Lankan "
        "company or person, even if they didn't ask about law. If the user hasn't said "
        "where the users or company are, ask them first; never guess the country. "
        "Send country codes and "
        "facts from get_fact_questions only (no idea text, no code). Returns warnings "
        "with severity (Must / Should / Check with a lawyer), the law and section, what "
        "to do, and the areas NOT covered."
    ),
)
def check_legal_risks(
    users_in: Annotated[
        list[str] | str,
        Field(description="ISO country codes where users are, as the user said, e.g. ['LK']"),
    ],
    facts: Annotated[
        list[str] | dict[str, bool] | str,
        Field(description="List of the facts that are true, from get_fact_questions"),
    ],
    company_in: Annotated[
        str | list[str] | None,
        Field(description="ISO country code where the company (or maker) is, e.g. 'LK'"),
    ] = None,
    processing_in: Annotated[
        list[str] | str | None,
        Field(description="ISO country codes where data is stored or processed"),
    ] = None,
    done: Annotated[
        list[str] | str | None,
        Field(
            description="rule_id values of warnings the user says are already handled. "
            "Only when the user says so; they are listed as 'done', not verified."
        ),
    ] = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    library = _get_library("check_legal_risks", ctx)
    all_facts = build_facts(users_in, facts, company_in, processing_in)
    try:
        result = check(library, all_facts, set(fact_list(done)))
    except FactError as exc:
        log.info("check rejected: %d unknown fact(s)", str(exc).count("'") // 2)
        usage.record("check_legal_risks", ctx, "error", reason="input")
        raise ToolError(str(exc)) from exc
    log.info("check: %d facts, %d warnings", len(all_facts), len(result["warnings"]))
    usage.record("check_legal_risks", ctx, facts=len(all_facts), **usage.check_counts(result))
    return result


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "List the facts check_legal_risks understands, grouped, each with the question "
        "it answers. Call once before check_legal_risks."
    ),
)
def get_fact_questions(ctx: Context | None = None) -> dict[str, Any]:
    library = _get_library("get_fact_questions", ctx)
    usage.record("get_fact_questions", ctx)
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
    ctx: Context | None = None,
) -> dict[str, Any]:
    library = _get_library("get_rule", ctx)
    rule = library.rules.get(rule_id)
    if rule is None:
        usage.record("get_rule", ctx, "error", reason="input")
        raise ToolError(f"No rule with id {rule_id!r}.")
    usage.record("get_rule", ctx, area=rule["area"])
    return {
        **{k: rule[k] for k in ("id", "title", "severity", "area", "why", "what_to_do")},
        "law": rule["law"],
        "in_force": rule["in_force"],
        "starts_on": str(rule["starts_on"]) if rule["starts_on"] else None,
        "last_checked": str(rule["last_checked"]),
        "review_status": rule["review_status"],
        "notes": rule.get("notes", ""),
    }


@mcp.tool(
    annotations=READ_ONLY,
    description=(
        "Get a law checklist for the product, for example the PDPA 2027 checklist: the rules "
        "of that law that apply to these facts, each with what to look for in the code "
        "(look_for) or ask the user (ask). Use it when the user asks whether their project "
        "is ready for the PDPA. Send country codes and facts only. Mark each item Found "
        "(with file and line), Missing or Can't tell from code; never give a score."
    ),
)
def get_checklist(
    users_in: Annotated[
        list[str] | str,
        Field(description="ISO country codes where users are, as the user said, e.g. ['LK']"),
    ],
    facts: Annotated[
        list[str] | dict[str, bool] | str,
        Field(description="List of the facts that are true, from get_fact_questions"),
    ],
    company_in: Annotated[
        str | list[str] | None,
        Field(description="ISO country code where the company (or maker) is, e.g. 'LK'"),
    ] = None,
    processing_in: Annotated[
        list[str] | str | None,
        Field(description="ISO country codes where data is stored or processed"),
    ] = None,
    law: Annotated[str, Field(description="Which checklist: 'pdpa'")] = "pdpa",
    ctx: Context | None = None,
) -> dict[str, Any]:
    library = _get_library("get_checklist", ctx)
    all_facts = build_facts(users_in, facts, company_in, processing_in)
    try:
        result = checklist(library, all_facts, law)
    except FactError as exc:
        log.info("checklist rejected")
        usage.record("get_checklist", ctx, "error", reason="input")
        raise ToolError(str(exc)) from exc
    log.info("checklist: %d facts, %d items", len(all_facts), len(result["items"]))
    usage.record(
        "get_checklist", ctx, facts=len(all_facts), items=len(result["items"]),
        client_items=len(result["client_items"]),
    )  # fmt: skip
    return result


def skill_text(name: str) -> str:
    """Steps shared with the skill (skills/rulewise/<name>), shipped in the package."""
    packaged = Path(__file__).resolve().parent / "skill" / name
    repo = Path(__file__).resolve().parents[2] / "skills" / "rulewise" / name
    return (packaged if packaged.is_file() else repo).read_text()


@mcp.prompt(
    name="check_project",
    title="Check my project with Rulewise",
    description=(
        "Read the whole project, find the facts, run the Rulewise check and write "
        "RULEWISE-REPORT.md with the warnings, the code they apply to and questions for a lawyer."
    ),
)
def check_project(ctx: Context | None = None) -> str:
    usage.record("prompt_check_project", ctx)
    return skill_text("check-project.md")


@mcp.prompt(
    name="pdpa_checklist",
    title="PDPA 2027 checklist",
    description=(
        "Check how ready the project's code is for Sri Lanka's PDPA and write "
        "RULEWISE-PDPA-CHECKLIST.md: X of Y items found in the code, top fixes, questions."
    ),
)
def pdpa_checklist(ctx: Context | None = None) -> str:
    usage.record("prompt_pdpa_checklist", ctx)
    return skill_text("pdpa-checklist.md")


def public_app(per_minute: int):
    """The hosted server: stateless HTTP (works across restarts and copies) behind a
    per-client request limit. Used by `rulewise --public`."""
    from .ratelimit import RateLimit

    app = mcp.streamable_http_app(stateless_http=True, json_response=True, host="0.0.0.0")
    return RateLimit(app, per_minute=per_minute)


def main() -> None:
    parser = argparse.ArgumentParser(prog="rulewise", description=__doc__.split("\n")[0])
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--public",
        action="store_true",
        help="hosted mode: HTTP on 0.0.0.0:$PORT, stateless, rate-limited, no access log",
    )
    args = parser.parse_args()
    # stderr only: stdout is the MCP channel in stdio mode. force=True: MCPServer() already
    # set up its own handler, which would drop the date that scripts/usage.py counts by day.
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", force=True
    )
    load()
    from . import web_api  # noqa: F401  registers /api/* routes for HTTP mode

    if args.public:
        import uvicorn

        per_minute = int(os.environ.get("RULEWISE_RATE_LIMIT", "60"))
        port = int(os.environ.get("PORT", args.port))
        # access_log=False: access logs would store client IP addresses (brief D6).
        uvicorn.run(public_app(per_minute), host="0.0.0.0", port=port, access_log=False)
    elif args.transport == "stdio":
        mcp.run("stdio")
    else:
        mcp.run("streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
