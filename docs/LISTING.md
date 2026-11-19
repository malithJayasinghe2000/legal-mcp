# Listing Rulewise in MCP directories

Free listings only (brief D10). Every result already says the rules are drafts, not yet
reviewed by a lawyer, so listing doesn't wait for the review. Malith submits with his own
accounts; nothing here is automated.

## 1. Official MCP Registry - done 2026-11-18 (v0.1.0)
File: [server.json](../server.json) (schema 2025-12-11, checked against the schema 2026-11-18).
It lists the hosted address only (`remotes`), so users install nothing.

```sh
brew install mcp-publisher
mcp-publisher login github      # as malithJayasinghe2000 (the name must start io.github.<that login>)
mcp-publisher publish           # from the repo root
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.malithJayasinghe2000/rulewise"
```

When the server address or version changes, raise `version` in `server.json` and publish again.
The registry checks the GitHub login, not the address, so a moved Azure address only needs a new publish.

## 2. Other directories
Some of these copy from the official registry; check each one after step 1 before adding by hand.
- **Smithery** (smithery.ai): add a remote server by its address.
- **Glama** (glama.ai/mcp/servers): finds GitHub repos; claim or add the repo.
- **PulseMCP** (pulsemcp.com): submit form.
- **Agensi**: list free. Don't sell it before a lawyer reviews the Must rules.

## 3. The Rulewise skill
[skills/rulewise/SKILL.md](../skills/rulewise/SKILL.md). Users install it with
`npx skills add malithJayasinghe2000/legal-mcp`. Skill directories (Agensi, skills.sh) list skills;
list it free there too.

Use the same short text everywhere:
> Rulewise warns developers which Sri Lankan laws apply to what they build (personal data,
> payments, AI, online content, consumer, e-commerce, cybercrime, copyright, lawyers and
> doctors). Legal information, not legal advice. Rules are drafts, not yet reviewed by a lawyer.

## Claude Code plugin versions
Raise `version` in `.claude-plugin/plugin.json` whenever the plugin changes (a new command, skill text or
server address). Users stay on the old version until it changes. 0.1.0: project check; 0.2.0: PDPA checklist; 0.2.1: Top 3 lists only Missing items; 0.2.2: clearer builds_for_client; 0.2.3: checklist parts all required.
