"""JSON API for the website, served by the same process as the MCP server (brief D7).

    GET  /api/health           rule count, or 503 if the library failed to load
    GET  /api/questions        guided questions (rules/questionnaire.yaml)
    POST /api/check            {users_in, company_in, processing_in, facts, done}
    GET  /api/rules/{rule_id}  one rule with its exact law quote

Store nothing (D6): request bodies are never logged or kept. A failed check is an
error (HTTP 4xx/5xx), never an empty "no issues" result.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from . import server
from .checker import FactError, build_facts, check

log = logging.getLogger("legal_check")
MAX_BODY = 20_000  # bytes; a full answer set is well under 2 KB
MAX_ITEMS = 100
NO_STORE = {"Cache-Control": "no-store"}


def _error(status: int, message: str) -> JSONResponse:
    return JSONResponse({"error": message}, status_code=status, headers=NO_STORE)


def _library_or_error():
    if server._library is None:
        return None, _error(
            503,
            "The rule library could not be loaded, so the check did NOT run. "
            "This is not a 'no issues found' result.",
        )
    return server._library, None


def _str_list(body: dict[str, Any], key: str) -> list[str]:
    value = body.get(key) or []
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        raise ValueError(f"'{key}' must be a list of at most {MAX_ITEMS} items")
    if not all(isinstance(v, str) and 0 < len(v) <= 60 for v in value):
        raise ValueError(f"'{key}' must contain short strings")
    return value


@server.mcp.custom_route("/api/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    library, err = _library_or_error()
    return err or JSONResponse({"status": "ok", "rules": len(library.rules)}, headers=NO_STORE)


@server.mcp.custom_route("/api/questions", methods=["GET"])
async def questions(request: Request) -> JSONResponse:
    library, err = _library_or_error()
    if err:
        return err
    if not library.questionnaire:
        return _error(503, "The question list is missing.")
    return JSONResponse(
        {"questionnaire": library.questionnaire, "areas": library.areas}, headers=NO_STORE
    )


@server.mcp.custom_route("/api/check", methods=["POST"])
async def check_route(request: Request) -> JSONResponse:
    library, err = _library_or_error()
    if err:
        return err
    raw = await request.body()
    if len(raw) > MAX_BODY:
        return _error(413, "Request too large.")
    try:
        body = json.loads(raw or b"{}")
        if not isinstance(body, dict):
            raise ValueError("body must be a JSON object")
        users_in = _str_list(body, "users_in")
        if not users_in:
            raise ValueError("'users_in' needs at least one country code")
        company_in = body.get("company_in")
        if company_in is not None and (not isinstance(company_in, str) or len(company_in) > 3):
            raise ValueError("'company_in' must be a country code")
        facts = build_facts(
            users_in, _str_list(body, "facts"), company_in, _str_list(body, "processing_in")
        )
        result = check(library, facts, set(_str_list(body, "done")))
    except (ValueError, FactError) as exc:  # json errors are ValueErrors too
        log.info("web check rejected")
        return _error(400, f"The check did not run: {exc}")
    log.info("web check: %d facts, %d warnings", len(facts), len(result["warnings"]))
    return JSONResponse(result, headers=NO_STORE)


@server.mcp.custom_route("/api/rules/{rule_id}", methods=["GET"])
async def rule_route(request: Request) -> JSONResponse:
    library, err = _library_or_error()
    if err:
        return err
    rule_id = request.path_params["rule_id"]
    if rule_id not in library.rules:
        return _error(404, "No rule with that id.")
    return JSONResponse(server.get_rule(rule_id), headers=NO_STORE)
