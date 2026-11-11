# Legal Check - instructions for Claude

An MCP server (plus a simple website later) that warns developers about the
**legal restrictions on what they are building**, starting with **Sri Lankan law**.
"Legal Check" is a working name.

**Read before doing anything:**
1. [docs/PROJECT-BRIEF.md](docs/PROJECT-BRIEF.md) - the idea, every decision made, limitations, future plans
2. [docs/ROADMAP.md](docs/ROADMAP.md) - what to build next (the current phase and step)
3. [docs/RULE-FORMAT.md](docs/RULE-FORMAT.md) - how rules are written
4. [docs/LEGAL-LANDSCAPE.md](docs/LEGAL-LANDSCAPE.md) - laws researched so far (unverified starting points)

When a decision changes or a step finishes, **update those docs in the same
change**, so the next chat has the right context.

## Code layout and commands
Python 3.12+, official MCP Python SDK v2 (`MCPServer`), managed with `uv`.
- `src/legal_check/` - the server package (MCP server comes in Step 4)
- `rules/<area>/` - the rule library (YAML, see RULE-FORMAT.md); `rules/facts.yaml` - facts triggers may use
- `tests/test_rules.py` checks every rule, including that its quote is word for word in the downloaded source
- `sources/sources.yaml` - official law sources; `sources/fetched.json` - what was downloaded and when
- `sources/raw/` - downloaded law files (not in git)
- `scripts/fetch_sources.py` - downloads the sources: `uv run --group sources python scripts/fetch_sources.py`
- `scripts/find_amendments.py` - checks Parliament for amendments not yet in sources.yaml: `uv run python scripts/find_amendments.py`
- Tests: `uv run pytest`. Lint/format: `uv run ruff check . && uv run ruff format .`

## Non-negotiable design rules
- **Rules first, AI second.** The rule library is the source of legal truth. AI
  only reads the idea, fills in facts and explains. It never invents a law. Plain
  RAG search is not the main engine (it misses laws the idea doesn't "sound like").
- **Never say "compliant" or "all clear".** Say "no issues found in the areas we
  cover" and list the areas not covered.
- **A failure is an error, never "no issues found".** If rules didn't load or a
  check couldn't run, return an error. (law-finder once reported an outage as
  "this law doesn't exist".)
- **Store nothing from users.** No ideas, no code, no request bodies in logs. Log counts and errors only.
- **Every rule has an official source link, an exact quote, a `last_checked`
  date and a review status.** Drafts are shown as "not yet reviewed by a lawyer".
- **Severity on every warning**: Must / Should / Check with a lawyer. Must items first.
- **Where the users are decides the law**, plus where the company is and where
  data is processed when a law says so (PDPA s.2 does). See brief D11.
- **Don't help evade laws.** Explain the law and the risk instead.
- **No referral fees or payment per client** if the product ever links to lawyers
  (Sri Lankan fee-sharing and touting rules; see law-finder).

## Working with Malith (the owner)
- He's a **software engineer, not a lawyer.** Do the legal reasoning yourself,
  pick the conservative defensible option, and explain it in plain language.
  Put truly unresolvable points in a "questions for a lawyer" list rather than blocking.
- **Explain short and simple, always.** Direct answer first, a few short bullets,
  no long tables. English is not his first language.
- **Verify by running, not reading.** Prove a feature works by running it for real
  (e.g. connect the MCP server to a real Claude Code session), not only by tests passing.
- **Don't start long local AI model runs** on his MacBook (it overheats). Ask first, prefer hosted.
- Launch-deferred features go **behind a one-line switch**, not deleted.
- In anything users see on the site: use "-", never the long dash "—".
- Git: remote `origin` = https://github.com/malithJayasinghe2000/legal-mcp (branch `main`).
  Malith allowed committing and pushing there when a piece of work is done (2026-11-11).

## Related project
`~/Developer/law-finder` is Malith's live Sri Lankan legal platform
(thelawyr.fiveneurals.com). It is the origin of this idea and **test case #1**.
Its law corpus (`lawyer-rag/data/acts/`) is mostly land, civil and criminal law, so
it barely overlaps with what this tool needs. Its legal research on Bar rules,
fee-sharing and AI advice is in `law-finder/lawyer-finder-web/docs/`.
**Don't modify law-finder from this project.**
