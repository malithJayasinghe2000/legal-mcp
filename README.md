# Legal Check (working name)

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

Status: Phase 1, collecting law sources. See [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) and [docs/ROADMAP.md](docs/ROADMAP.md).
