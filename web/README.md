# Rulewise website

Guided questions in, a cited legal report out (brief D17). **For now (D21) the site is a home
page for the MCP server; `/check` is hidden by `SHOW_SITE_CHECK` in `src/lib/features.ts`.** The site has no checker of
its own: it forwards `/api/*` to the Python server, the same one Claude Code uses.
Design plan: [../docs/WEBSITE-DESIGN.md](../docs/WEBSITE-DESIGN.md).

## Run it locally

```sh
# 1. The checker API (from the repo root)
uv run rulewise --transport streamable-http --port 8100

# 2. The site (from web/)
npm install
RULEWISE_API_URL=http://127.0.0.1:8100 npm run dev -- --port 3100
```

Open http://127.0.0.1:3100. (Ports 3000/8000 are often taken by other projects.)

## Checks

```sh
npm run lint
npm run typecheck
npx playwright install chromium   # once
npm run test:e2e                  # needs both servers running; desktop + mobile, axe a11y
```

Screenshots from the e2e run land in `test-results/screens/` for design review.

## Rules for this site
- Use "-", never the long dash, in anything users see.
- Orange `#F57E22` only as a fill with ink text; orange text uses `orange-deep`.
- No analytics, cookies or local storage of answers. A failed check shows an error,
  never "no issues".
