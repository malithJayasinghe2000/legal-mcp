# Rulewise

Legal issue-spotting for people who build software. Connect it to your AI
coding tool (Claude Code, Cursor, VS Code) as an MCP server. While you build, it
tells you which laws apply to what you're building, how serious each one is, and
what to ask a lawyer. Starts with Sri Lankan law.

It gives legal information, not legal advice.

## Setup

Needs [uv](https://docs.astral.sh/uv/).

```sh
uv sync                                                  # install
uv run pytest                                            # tests
uv run --group sources python scripts/fetch_sources.py   # download the law sources
```

## Use it in Claude Code (local)

```sh
claude mcp add rulewise -- uv run --directory /path/to/legal-check rulewise
```

Then just describe what you're building. Claude calls the `check_legal_risks` tool
when you plan a feature for a product used in Sri Lanka. The server receives only
facts and country codes, never your idea text or code, and stores nothing.

Tools: `check_legal_risks`, `get_fact_questions`, `get_rule` (exact law quote + link).

## Website

See [web/README.md](web/README.md): guided questions, same checker, nothing stored.

Status: Phase 1. 42 draft rules in 6 areas (not yet reviewed by a lawyer). Website runs locally; not hosted yet. See [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) and [docs/ROADMAP.md](docs/ROADMAP.md).
