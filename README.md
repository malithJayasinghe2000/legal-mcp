# Rulewise

Legal issue-spotting for people who build software. Connect it to your AI
coding tool (Claude Code, Cursor, VS Code) as an MCP server. While you build, it
tells you which laws apply to what you're building, how serious each one is, and
what to ask a lawyer. Starts with Sri Lankan law.

It gives legal information, not legal advice.

## Use it

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (once):
   - Mac / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Add Rulewise to your AI tool. It installs straight from GitHub; no need to download the code.
   - **Claude Code:**
     ```sh
     claude mcp add rulewise -- uvx --from git+https://github.com/malithJayasinghe2000/legal-mcp rulewise
     ```
   - **Cursor** (`~/.cursor/mcp.json`), **VS Code** (`.vscode/mcp.json`, key `servers`),
     **Codex** (`~/.codex/config.toml`): command `uvx`, args
     `["--from", "git+https://github.com/malithJayasinghe2000/legal-mcp", "rulewise"]`.
3. Restart the tool. The first start takes about 30 seconds while it downloads.

Then just describe what you're building and where your users are. Claude calls the `check_legal_risks` tool
when you plan a feature for a product used in Sri Lanka. The server receives only
facts and country codes, never your idea text or code, and stores nothing.

Tools: `check_legal_risks`, `get_fact_questions`, `get_rule` (exact law quote + link).

## Develop

```sh
uv sync                                                  # install
uv run pytest                                            # tests
uv run --group sources python scripts/fetch_sources.py   # download the law sources
claude mcp add rulewise -- uv run --directory /path/to/legal-check rulewise   # use your local copy
```

## Website

See [web/README.md](web/README.md). For now it is a home page with setup steps; the guided check is hidden (brief D21).

Status: Phase 1. 57 draft rules in 9 areas (not yet reviewed by a lawyer). Website runs locally; not hosted yet. See [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) and [docs/ROADMAP.md](docs/ROADMAP.md).
