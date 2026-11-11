# Roadmap

Decisions behind this plan: [PROJECT-BRIEF.md](PROJECT-BRIEF.md).

## Phase 0 - Setup (done 2026-11-11)
- [x] New repo, project brief, roadmap, legal landscape, rule format, CLAUDE.md

## Phase 1 - First working version (Sri Lanka, 4-5 areas)

Goal: a developer connects the MCP server in Claude Code, describes a feature, and
gets correct warnings. law-finder's story is the first test.

### Step 1. Collect the law sources
- Download the official texts listed in [LEGAL-LANDSCAPE.md](LEGAL-LANDSCAPE.md)
  section "Sri Lanka - laws to collect" for the first areas.
- Store them with their source URL and download date.
- Big PDFs: put them in storage outside git, or decide deliberately to track
  them (law-finder tracked its vector store in git, and that was messy).
- Check the law-finder corpus for anything reusable: Companies Act, and probably
  the Computer Crime Act (`law-finder/lawyer-rag/data/acts/24-2007_E.pdf`, check first).

### Step 2. First 5 areas, about 30-50 rules
1. **Personal data**: Personal Data Protection Act No. 9 of 2022
2. **Payments and finance**: Central Bank rules, Payment and Settlement Systems Act
3. **AI features**: AI giving advice, profiling, automated decisions, disclosure
4. **Online content**: Online Safety Act No. 9 of 2024, user-generated content
5. **Regulated professions**: lawyers (Supreme Court rules 1988, Intermeddlers
   Ordinance), doctors (Medical Council)

AI drafts each rule from the source text, and Malith checks it against the source.
Every rule starts as `review_status: draft`. Format: [RULE-FORMAT.md](RULE-FORMAT.md).

### Step 3. Fact questions (first draft)
- Where are your users? (country list, default `LK`)
- Who are the users? (public / businesses / children / employees)
- Personal data collected? Which kinds? (contact, NIC / passport, health,
  financial, location, biometric, children's data)
- Payments? (take payments, hold money, lend, crypto)
- AI features? (chatbot, advice, decisions about people, generated content)
- Regulated profession involved? (law, medicine, finance, education...)
- User-generated content or messaging?
- Data sent outside Sri Lanka? (cloud region, foreign AI APIs)

### Step 4. The MCP server
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

### Step 5. Test set
- 20-30 example ideas with expected warnings, run with one command.
- **Test case #1: law-finder** (lawyer directory + client chat + AI legal Q&A +
  subscriptions, users in Sri Lanka). Must catch:
  - Supreme Court Rules 1988: Rule 45 (directories allowed), Rule 49 (practice details), Rule 39 (touting)
  - Fee-sharing: no charging per client / enquiry / message
  - Intermeddlers with Suitors Ordinance s.2: no payment for bringing clients
  - AI legal advice on a non-lawyer platform (BASL note, June 2021)
  - Personal Data Protection Act: client and user data
- Test case #2: doctor booking app with online payment and medical history.
- Test case #3: student project with a chatbot, no personal data. Should give few or no warnings.
- Prove it by **running it from a real Claude Code session**, not just unit tests.

### Step 6. Simple website
- Paste an idea, answer the fact questions, get the same report. Same backend.

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
