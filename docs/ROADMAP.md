# Roadmap

Decisions behind this plan: [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## Phase 0 - Setup (done 2026-11-11)
- [x] New repo, project brief, roadmap, legal landscape, rule format, CLAUDE.md

## Phase 1 - First working version (Sri Lanka, 4-5 areas)

Goal: a developer connects the MCP server in Claude Code, describes a feature, and
gets correct warnings. law-finder's story is the first test.

- [x] Language decided: Python + official MCP SDK v2 + uv (brief D12). 2026-11-11
- [x] Project structure set up (see CLAUDE.md "Code layout"). 2026-11-11

### Step 1. Collect the law sources (mostly done 2026-11-11)
- [x] Official sources for the first 5 areas listed in [sources/sources.yaml](../sources/sources.yaml),
  each with URL and what was verified in the document itself.
- [x] Download script: `uv run --group sources python scripts/fetch_sources.py`.
  11 of 15 download from official sites and were checked (title, number, date). Record in `sources/fetched.json`.
- [x] Decided: PDFs stay **out of git** (`sources/raw/`); git keeps the URL, date
  and sha256, so anyone can re-download the same version.
- [x] law-finder's `24-2007_E.pdf` is the Computer Crime Act No. 24 of 2007 (checked). Not in the first 5 areas.
- [ ] **Malith, manual (4 items):**
  1. ~~Attorneys-at-Law Rules 1988~~ done 2026-11-11 (manual browser download).
  2. ~~PDPA commencement Gazette No. 2498/16~~ done 2026-11-11 (found on dpa.gov.lk; start date verified).
  3. BASL note (June 2021): no copy online. Ask BASL or the lawyer reviewer.
  4. ~~Intermeddlers Ordinance from CommonLII~~ done 2026-11-11 (manual browser download).
- Official sources only, same rule as law-finder: never lankalaw.net or other private sites.
- [x] Automatic amendment search: `uv run python scripts/find_amendments.py` searches
  Parliament's acts listing for every main law and fails if an amendment is missing. 2026-11-11 result:
  nothing missing. Payment Act No. 28 of 2005 has **no amendments**. Medical Ordinance:
  SLMC copy includes amendments up to 2018, plus Act No. 46 of 2024 separately.
- [ ] When writing PDPA rules, read each cited section together with Amendment No. 22 of 2025.

### Step 2. First 5 areas, about 30-50 rules
1. **Personal data**: Personal Data Protection Act No. 9 of 2022
2. **Payments and finance**: Payment and Settlement Systems Act No. 28 of 2005,
   Payment Cards and Mobile Payment Systems Regulations No. 1 of 2013, MVTS Regulations No. 01 of 2025
3. **AI features**: AI giving advice, profiling, automated decisions (PDPA s.18, s.24), disclosure
4. **Online content**: Online Safety Act No. 9 of 2024, user-generated content
5. **Regulated professions**: lawyers (Supreme Court rules 1988, Intermeddlers
   Ordinance Cap. 40), doctors (Medical Ordinance Cap. 105 + Amendment No. 46 of 2024, SLMC guidelines)

AI drafts each rule from the source text, and Malith checks it against the source.
Every rule starts as `review_status: draft`. Format: [RULE-FORMAT.md](RULE-FORMAT.md).

Progress:
- [x] **Personal data: 16 rules** in `rules/personal-data/` (2026-11-11). Quotes checked
  word for word against the downloaded Act by `tests/test_rules.py`. All `in_force: false`:
  Part I/III start 1 Jan 2027 (verified in Gazette 2498/16); Part II rights and Part IV marketing have no date.
- [ ] Malith: check the 16 personal data rules against the Act, set `review_status: checked_by_owner`.
- [x] **Payments: 4 rules** in `rules/payments/` (2026-11-11): card gateway, wallet/cards licence,
  marketplace payouts, money transfer. Not covered yet: lending (Finance Business Act),
  crypto, Foreign Exchange Act, Central Bank circulars (e-money limits, app security).
- [ ] Malith: check the 4 payment rules, and the typed copy of the scanned 2018 Direction
  (`sources/transcripts/`) against the PDF.
- [x] **AI features: 3 rules** in `rules/ai/` (2026-11-11): training on user data (PDPA s.6),
  AI acting as a doctor (Medical Ordinance s.38), bots (Online Safety Act s.22). Already in
  personal data: automated decisions, profiling impact assessment, sending data to foreign AI APIs.
  **AI giving legal advice** waits for the 1988 Rules PDF and the BASL note (regulated professions).
  Sri Lanka has no AI law, so no rule on telling users they talk to an AI (EU AI Act Art. 50 is Phase 3).
- [x] **Online content: 2 rules** in `rules/online-content/` (2026-11-11): 24-hour takedown
  (OSA s.23(8)), losing intermediary protection (s.27(3)). Plus bots in `rules/ai/`.
  Not covered yet: paid content on "declared online locations" (s.29), user offences (s.12-21).
- [x] **Regulated professions - doctors: 4 rules** in `rules/regulated-professions/` (2026-11-11):
  directory open to all (SLMC misconduct item v), no paid promotion of named doctors (SLMC 4.3),
  no commission per patient (SLMC ethics), registered doctors only (Medical Ordinance s.38(b)).
  Not collected yet: SLMC Social Media Guidelines, Nov 2025 advertising notice, telemedicine gazette.
- [x] **Regulated professions - lawyers: 6 rules** (2026-11-11): directory details (Rule 45/40),
  no practice particulars (Rule 49), no paid promotion (Rule 39(2)), no fee per client
  (Rule 39(1)), Intermeddlers s.2(a) (criminal, applies to the platform), online/AI legal advice
  (Rule 39 + BASL note, "check with a lawyer"). The 1988 Rules have **no separate fee-sharing
  rule**: law-finder's fee-sharing problem comes from Rule 39(1) and Intermeddlers s.2.
- [x] **Consumer rights: 6 rules** in `rules/consumer/` (2026-11-12): misleading conduct (s.30),
  false claims and fake discounts (s.31), implied warranty and refunds (s.32), receipts (s.28),
  tied selling (s.16(b)), trader registration (s.27, "check with a lawyer"). New facts
  `sells_to_consumers`, `sells_goods`. The 2003 Act on parliament.lk is a scanned PDF: quotes come
  from a typed copy `sources/transcripts/lk-caa-2003.txt`. Amendment No. 20 of 2021 only changes
  penalties (s.60). Not covered yet: CAA directions and gazetted price controls.
- [ ] Malith: check the typed copy of the CAA Act against the scanned PDF, then the 6 rules.
- **Total: 42 rules in 6 areas.**

### Step 3. Fact questions (first draft)
Machine-readable list: [rules/facts.yaml](../rules/facts.yaml) (grows as areas are added).
- Where are your users? (country list, default `LK`)
- Where is your company, and where is data processed / hosted? (PDPA s.2 applies
  to Sri Lankan companies and processing in Sri Lanka even with foreign users)
- Who are the users? (public / businesses / children / employees)
- Personal data collected? Which kinds? (contact, NIC / passport, health,
  financial, location, biometric, children's data)
- Payments? (take payments, hold money, lend, crypto)
- AI features? (chatbot, advice, decisions about people, generated content)
- Regulated profession involved? (law, medicine, finance, education...)
- User-generated content or messaging?
- Data sent outside Sri Lanka? (cloud region, foreign AI APIs)

### Step 4. The MCP server (done 2026-11-11)
Built in `src/legal_check/` (`library.py` loads and validates rules, `checker.py` matches,
`server.py` has the 3 tools). Input is facts + country codes only (brief D16).
**Verified in a real Claude Code session** (headless, empty folder, prompt about a doctor
booking app that never mentioned law): Claude called `get_fact_questions` and
`check_legal_risks` by itself, got 16 warnings, explained Must first with sections, said
the rules are drafts, listed areas not covered, and flagged the per-booking doctor fee
(SLMC commission rule) as a business-model problem.
**"Done" items (2026-11-11):** `check_legal_risks` takes `done` (rule ids the user says are
handled). They move to a "done" list with a `done_check` reminder; never verified, never
"no issues". Real session: user said the privacy notice was done; Claude listed it as
"already handled (not checked)" with what to double-check, and kept the other 7. (It did
this in its answer; `done` is used on later checks once rule ids are known.)
Not done yet: HTTP hosting (Step 6 / launch), API keys.

Original plan:
- Tool `check_legal_risks`: input = feature/idea text + facts + users' countries.
  Output = matched warnings (severity, why, law + section + link, what to do,
  lawyer questions), plus areas covered and **areas not covered**.
- Tool `get_fact_questions`: returns the questions to ask the developer.
- Tool `get_rule`: full rule + exact law text (proof).
- Short, broad tool description: "Call whenever the user plans or builds a feature
  for a product used in Sri Lanka."
- Server instructions: ask where users are and what data is collected at the start.
- Store nothing. Log counts and errors only.
- **A failure returns an error, never "no issues found".**

### Step 5. Test set (started 2026-11-11)
`tests/cases.yaml` has 5 cases (law-finder #1 marked pending until lawyer rules exist;
#2 doctor booking, #3 student chatbot, #4 Sri Lankan company with EU users,
#5 foreign-only), plus #6-#25 added 2026-11-11 (shop, wallet, marketplace, teen social app,
school system, HR SaaS, loan app, AI symptom checker, telemedicine, clinic directory, chatbot
training, news bot, CCTV face recognition, ride-hailing, SMS marketing, remittance, US company,
AI legal drafting, outsourcing team, static site). All 26 pass; no wrong-area warnings.
Findings to decide:
  - **Noise (decided 2026-11-11: keep separate).** Every app with personal data gets the same
    8 basic PDPA warnings. Malith found a grouped "basics" item harder to understand, and in
    real sessions Claude already groups them when explaining. So each stays its own warning.
  - **Done 2026-11-11: building for a client.** Fact `builds_for_client`; rules have
    `duty_of: controller | processor | both`. Controller duties move to a separate
    "client_duties" list (not hidden), and the builder gets `lk-pdpa-processor-duties`
    (s.22). Verified in a real session (Colombo company building a hospital app).
  - **Gap:** lending licences (#12), crypto, foreign exchange.
  - **Trigger test on small coding requests (2026-11-11), real headless sessions** in a small
    fake project (README: clinic booking app for patients in Sri Lanka). 6 requests:
    NIC field, diagnosis columns, PayHere payments, OpenAI symptom chat, Friday promo SMS
    -> all 5 called check_legal_risks with sensible facts; "centre the header CSS" -> no call.
    The AI symptom chat request was paused for the user's decision (Medical Ordinance s.38)
    with a safer design; the NIC request was built, with the relevant PDPA warnings.
    Not tested yet: projects with no hint of Sri Lanka in the files (layer 3 asks then). Case #1 (law-finder, original and fixed design) passes, and **passed in a
real Claude Code session** (2026-11-11): it flagged the per-enquiry fee (Rule 39(1) +
Intermeddlers s.2), featured slots (Rule 39(2)), past cases/ratings (Rule 49) and the AI
legal chat (BASL note), then designed the schema without them. Run: `uv run pytest tests/test_server.py`. Grow it to 20-30.

Original plan:
- 20-30 example ideas with expected warnings, run with one command.
- **Test case #1: law-finder** (lawyer directory + client chat + AI legal Q&A +
  subscriptions, users in Sri Lanka). Must catch:
  - Supreme Court Rules 1988: Rule 45 (directories allowed), Rule 49 (practice details), Rule 39 (touting)
  - Fee-sharing: no charging per client / enquiry / message
  - Intermeddlers with Suitors Ordinance s.2 (esp. 2(c): a non-lawyer taking payment for
    procuring a lawyer's employment): no payment for bringing clients
  - AI legal advice on a non-lawyer platform (BASL note, June 2021)
  - Personal Data Protection Act: client and user data
- Test case #2: doctor booking app with online payment and medical history.
- Test case #3: student project with a chatbot, no personal data. Should give few or no warnings.
- Prove it by **running it from a real Claude Code session**, not just unit tests.

### Step 6. Simple website
- Discussed 2026-11-11: guided questions, no AI (D17); light base + orange `#F57E22` (D18);
  Next.js/Tailwind/shadcn stack (D19). Design skill installed: `.claude/skills/frontend-design`.
  Product name: Rulewise (D20). Still open: domain, hosting.
- **Built 2026-11-12 (first version, local):** `web/` (Next.js 16). Home page; `/check` guided
  questions (6 steps, from `rules/questionnaire.yaml`); report with marginal-note layout,
  "at a glance" list, exact law quote on demand, mark as done, client duties, coverage,
  print/PDF. Python serves the JSON API (`/api/*`, `src/legal_check/web_api.py`) next to `/mcp`.
  Tests: Python API tests (errors are errors, no input in logs) + Playwright e2e on desktop and
  mobile with axe accessibility checks (0 violations). Not done: hosting, domain.
- **Changed 2026-11-12 (D21): MCP first.** `/check` is hidden behind `SHOW_SITE_CHECK`
  (`web/src/lib/features.ts`), not deleted. Home page now explains the MCP server and shows
  setup for Claude Code, Cursor, Codex and VS Code; example is an online shop (promo SMS,
  privacy notice). Later: bring the site check back as "describe your idea" (our LLM) and/or
  questions that depend on the product type.
- **Next for the MCP server (agreed 2026-11-12):** (1) more general areas: consumer rights (done
  2026-11-12), e-commerce and online contracts, cybercrime and security, copyright; (2) Malith reviews the
  36 draft rules; (3) remote hosting with a usage limit, so it works by web address in
  Claude, ChatGPT, Cursor, Codex; (4) setup guide per tool; (5) lawyer review before launch.
- Order agreed 2026-11-11: test set (Claude) + rule check (Malith, in parallel) -> website -> lawyer review of Must rules.

### Step 7. Before public launch
- A lawyer reviews the Must rules in the 5 areas.
- Terms of service + privacy policy (information, not legal advice; stores nothing).
- Open-source the server code.
- Show it to 10-20 real developers, and **watch whether they keep using it**.

## Phase 2 - Grow (only if Phase 1 gets real use)
- Generate documents: privacy policy, consent text, terms, data protection checklist.
- More Sri Lankan areas: consumer, e-commerce, copyright, telecom, children, employment, crypto, tax.
- Daily watcher for Gazette / Parliament / Central Bank updates, flagging affected rules.
- Feedback button on warnings.
- Local mode (rules downloaded, runs offline).

## Phase 3 - Paid and wider
- Foreign laws: GDPR, EU AI Act, UK, Australia (for Sri Lankan software companies).
- Standards layer: ISO/IEC 42001, NIST AI RMF.
- "Send to lawyer" report.
- Code scanning, GitHub check, VS Code extension.
- University partnerships.
- API keys, team accounts, pricing.
- Other South Asian countries.
