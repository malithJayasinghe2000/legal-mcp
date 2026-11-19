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
  Codex doesn't follow the server's own instructions, so also add the Rulewise skill
  ([skills/rulewise/SKILL.md](skills/rulewise/SKILL.md)), or it only uses Rulewise when asked:
  `npx skills add malithJayasinghe2000/legal-mcp` (asks which AI tools to install it into).
  Without Node.js, add this line to `AGENTS.md` instead (project, or `~/.codex/AGENTS.md`):
  `Before planning or building a product or feature, check it with the Rulewise MCP tools (get_fact_questions, then check_legal_risks).`

Prefer to run it on your own computer? Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:
```sh
claude mcp add rulewise -- uvx --from git+https://github.com/malithJayasinghe2000/legal-mcp rulewise
```

Then just describe what you're building and where your users are. Claude calls the `check_legal_risks` tool
when you plan a feature for a product used in Sri Lanka. The server receives only
facts and country codes, never your idea text or code, and stores nothing.

Tools: `check_legal_risks`, `get_fact_questions`, `get_rule` (exact law quote + link).

### Check a whole project

Already built something? Ask your AI tool to check the whole project. It reads your code on
your computer, sends Rulewise only the facts it found, and writes `RULEWISE-REPORT.md`: Must,
Should and Check with a lawyer items, the file each one applies to, what to fix first and
questions for a lawyer.

- **Claude Code plugin** (the server, the skill and `/rulewise:check` in one install; use it
  instead of the `claude mcp add` line above):
  ```
  /plugin marketplace add malithJayasinghe2000/legal-mcp
  /plugin install rulewise@rulewise
  ```
  In the VS Code panel `/plugin` isn't available yet; run this in a terminal instead:
  ```sh
  claude plugin marketplace add malithJayasinghe2000/legal-mcp
  claude plugin install rulewise@rulewise
  ```
  Then reload the window and run `/rulewise:check`.
- **Codex, Copilot and others with the Rulewise skill:** say "check my project with Rulewise".
- **Tools that show MCP prompts:** the server's `check_project` prompt does the same.
- **Any tool with the server:** "Check this project with Rulewise and write a report" works too.

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

Status: Phase 1. 61 draft rules in 11 areas (not yet reviewed by a lawyer). Website: https://legal-mcp.vercel.app. MCP server hosted on Azure. See [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) and [docs/ROADMAP.md](docs/ROADMAP.md).

## Licence

[MIT](LICENSE). The rules are legal information, not legal advice; they are provided "as is",
without warranty (see the licence and the [privacy and terms page](https://legal-mcp.vercel.app/privacy)).
