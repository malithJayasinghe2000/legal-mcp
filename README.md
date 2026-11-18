# Rulewise

Legal issue-spotting for people who build software. Connect it to your AI
coding tool (Claude Code, Cursor, Codex, VS Code) as an MCP server. While you build, it
tells you which laws apply to what you're building, how serious each one is, and
what to ask a lawyer. Starts with Sri Lankan law.

It gives legal information, not legal advice.

## Use it

Nothing to install. Add the hosted server to your AI tool:

- **Claude Code:**
  ```sh
  claude mcp add --transport http rulewise https://rulewise.victoriousdune-a7b660c5.centralindia.azurecontainerapps.io/mcp
  ```
- **Cursor** (`~/.cursor/mcp.json`, `{"mcpServers": {"rulewise": {"url": "<address>"}}}`),
  **VS Code** (`.vscode/mcp.json`, `{"servers": {"rulewise": {"type": "http", "url": "<address>"}}}`),
  **Codex** (`~/.codex/config.toml`, `[mcp_servers.rulewise]` with `url = "<address>"`).
  Codex doesn't follow the server's own instructions, so also add this line to `AGENTS.md`
  (project, or `~/.codex/AGENTS.md`), or it only uses Rulewise when asked:
  `Before planning or building a product or feature, check it with the Rulewise MCP tools (get_fact_questions, then check_legal_risks).`

Prefer to run it on your own computer? Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:
```sh
claude mcp add rulewise -- uvx --from git+https://github.com/malithJayasinghe2000/legal-mcp rulewise
```

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

## Host it

See [docs/DEPLOY-AZURE.md](docs/DEPLOY-AZURE.md) (Docker, Azure Container Apps).

## Website

See [web/README.md](web/README.md). For now it is a home page with setup steps; the guided check is hidden (brief D21).

Status: Phase 1. 57 draft rules in 9 areas (not yet reviewed by a lawyer). Website: https://legal-mcp.vercel.app. MCP server hosted on Azure. See [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) and [docs/ROADMAP.md](docs/ROADMAP.md).
