# Project Brief - Legal Check

Everything decided in the first planning conversation (2026-11-11), so any new
chat can continue without losing context. "Legal Check" is a working name only.

Related docs:
- [ROADMAP.md](ROADMAP.md) - what to build first, and what comes later
- [LEGAL-LANDSCAPE.md](LEGAL-LANDSCAPE.md) - the laws researched so far (Sri Lanka + AI laws worldwide)
- [RULE-FORMAT.md](RULE-FORMAT.md) - how a rule in the rule library is written

---

## 1. Where the idea came from

Malith built **law-finder** (a Sri Lankan legal platform, live at
thelawyr.fiveneurals.com, repo `~/Developer/law-finder`) on his own. When lawyers
looked at it, they found laws and restrictions he did not know about. He had to
research again and change the project scope and features.

Examples of what was found late on law-finder:
- **Bar rules on lawyer directories and advertising.** Supreme Court (Conduct of
  and Etiquette for Attorneys-at-Law) Rules 1988: Rule 45 allows directories,
  Rule 49 limits publishing details of a lawyer's practice, Rule 39 bans touting.
- **Fee-sharing.** Charging per client, enquiry or message counts as sharing a
  lawyer's fees. law-finder had to change to selling software seats to firms only.
- **Intermeddlers with Suitors Ordinance.** Taking payment for bringing clients to
  a lawyer is an offence.
- **AI giving legal advice.** A BASL (Bar Association) note from June 2021 says legal
  advice through public non-lawyer online platforms can be touting. The AI chat
  had to be restricted and controlled on the server.
- **Personal data** law applies to user and client data.

**The problem in general:** many people now build systems with AI, and most of
them don't know the laws and ethics of the area they are building in. They find
out late, or never.

## 2. The idea

A tool that gives **legal suggestions and restrictions while someone is building
a system**. It connects to the developer's AI coding tool (Claude Code, Cursor, VS
Code) as an **MCP server**.

Simple example:
1. Developer: "I'm building a lawyer-finding app for Sri Lanka."
2. Tool: "Lawyers can't advertise freely (Bar rules). Don't take a share of
   lawyers' fees. You collect personal data, so the data protection law applies.
   Ask a lawyer these 3 questions before launch."
3. The developer fixes the plan before writing code.

**It is a warning system, not a lawyer.** It says what to check, with the law
behind each point. It never says "you are compliant."

## 3. Existing tools (researched 2026-11-11)

Parts of the idea exist. The whole idea does not.

| Kind | Examples | Limit |
|---|---|---|
| Code scanners for personal data | Privado (open source), Bearer, HoundDog.ai | Privacy only, mostly GDPR, code must already exist |
| EU AI Act checkers | EU official questionnaire, Aguardic, ark-forge/mcp-eu-ai-act (MCP) | One law, one region |
| Small legal MCP servers | Glama "legal & compliance" list, Open Legal Compliance MCP, us-law-mcp | Hobby projects, mostly US law lookup |
| Security compliance platforms | Vanta, Drata | SOC 2 / ISO audits, not "is my product legal" |

**The gap (our position):**
- Starts at the **idea stage**, before code.
- Covers **all legal areas** (professional rules, payments, data, AI, consumer, content...),
  not one law.
- Covers **Sri Lanka**, which no tool covers. None of the tools above would have
  caught law-finder's Bar rules or fee-sharing problems.

Code scanning is easy for others to copy. The local law knowledge is the hard part and the edge.

Sources: glama.ai/mcp/servers/categories/legal-and-compliance,
github.com/ark-forge/mcp-eu-ai-act, privado.ai, bearer.com, hounddog.ai,
artificialintelligenceact.eu, aguardic.com.

## 4. Decisions made

| # | Decision | Why |
|---|---|---|
| D1 | **Separate repo** (`~/Developer/legal-check`), not inside law-finder | Different product, different users. law-finder is live and must not be risked. Can be open-sourced on its own. |
| D2 | **Sri Lanka law only** for the first version | The gap is there, and we have the local knowledge. Other countries come later. |
| D3 | **Rules first, AI second** (not plain RAG) | See section 6. Plain RAG search misses laws the idea doesn't "sound like". |
| D4 | **Reuse only law *text* from law-finder, not its RAG design** | law-finder answers questions about law. This tool must find *every* law that applies to an idea. Different problem. |
| D5 | **Start without lawyers**: AI drafts rules from official sources, Malith checks them against the source text, and every rule is marked "not yet reviewed by a lawyer". **A lawyer reviews the main areas before public launch.** | Lawyers are needed because acts don't say when they apply to an app, and many restrictions are outside acts (Bar rules, Central Bank directions, practice). But that shouldn't block starting. |
| D6 | **Store nothing** from users: no ideas, no code, no request bodies | Trust. Developers send unreleased ideas. |
| D7 | **First delivery: MCP server + simple website**, sharing one backend | The website brings people in; the MCP server is what makes it different. |
| D8 | **Severity levels on every warning**: Must / Should / Check with a lawyer | Without levels, developers get overwhelmed and ignore everything. |
| D9 | **Update by automated checking, human changing**: a script watches official sources daily and flags affected rules; a human edits rules | Wrong or outdated rules are the biggest accuracy risk. |
| D10 | **Free first.** Prove people use it before charging. | Sri Lankan market is small and developers rarely pay. |
| D11 | **Where the users are decides which laws apply** - and also where the company is and where data is processed, when a law says so | That's how the EU AI Act and GDPR work. The tool must ask "where are your users?" **Correction (2026-11-11):** PDPA s.2(1) also applies when processing happens in Sri Lanka, or the company is incorporated, domiciled or resident in Sri Lanka, even if all users are abroad. So the tool also asks where the company is and where data is processed. |
| D12 | **Python, official MCP Python SDK (v2), managed with `uv`** | Law-processing tools (PDF text, scripts) are Python. The server is small, deterministic matching, so speed doesn't matter. The official SDK v2 includes the old FastMCP as `MCPServer` (`from mcp.server.mcpserver import MCPServer`). TypeScript would only win for a browser extension, which isn't planned. |
| D13 | **Only software-relevant laws, never all Sri Lankan law** (2026-11-11). MVP: 5 areas, about 15 documents; later 15-20 areas. Land, family and most criminal law are out. | The tool spots risks for apps. Laws are read to **write rules**; they are not fed into an AI or kept as a library. |
| D14 | **Any site for research; official text for rules** (2026-11-11). Private copies (lankalaw.net etc.) may be used to find and read laws. A rule's `quote` and `source_url` must come from an official copy (Parliament, regulator, Gazette, CommonLII, LawNet). | Unlike law-finder, we don't republish law files, so copyright isn't the issue. But users see the link and quote, so they must be trustworthy; private copies can be old or have scan errors. |
| D15 | **Automate source collection for the MVP** (2026-11-11). Claude finds and downloads main laws and their amendments by script (Parliament's acts listing), and reads main law + amendments together. Malith only fetches files that sites block or that aren't online, and checks each rule against its source (D5). | No manual library work like law-finder. No government site has an up-to-date consolidated text, so we combine main law + amendments ourselves. |
| D16 | **The server takes only facts and country codes, never the idea text or code** (2026-11-11). | Matching needs only facts, so asking for text would collect user data for nothing (D6). Claude on the developer's side reads the idea and picks the facts. An unknown fact is an error, not ignored, because ignoring it could hide a law. |

## 5. How it works (simple)

### What MCP is
MCP is a standard way to give an AI coding tool **extra tools**. Claude Code has
built-in tools (read files, run commands). Our MCP server adds our own tool, for
example `check_legal_risks`.

### Step by step
1. **Developer connects once**:
   `claude mcp add --transport http legal-check https://<our-server>/mcp`
   (Cursor: a few lines in its MCP settings file.)
2. **When Claude Code starts**, it asks our server for its tools. Our server
   returns each tool's name, description, inputs, and **server instructions**.
3. **Developer chats as normal**: "add online payments for doctor bookings".
4. **Claude decides on its own** to call our tool and sends structured facts:
   ```json
   { "feature": "doctor booking with online payment",
     "users_in": ["LK"],
     "facts": ["collects_personal_data", "health_data", "takes_payments", "regulated_profession:medicine"] }
   ```
   The first time, Claude Code asks the developer to allow the tool.
5. **Our server matches the facts against the rule library** and returns warnings
   with severity, law, reason, source link and questions for a lawyer.
6. **Claude explains the result** in simple words and helps change the plan or code.

### Who does what
- **Developer**: talks to Claude.
- **Claude (on the developer's side)**: understands the idea, picks out the facts,
  calls our tool, explains the answer.
- **Our server**: the **source of legal truth**. It holds the rules and returns
  the matching ones. Claude must only explain what our server returns, never
  invent laws.

Because Claude on the developer's side does the language work, **our server may not
need an AI model at all**. Matching is deterministic, so it's cheap to run and
can run locally.

### How it gets triggered when the developer doesn't ask
Developers won't say "check my idea". They say "store the NIC number" or just start coding.
1. **A broad tool description**: "Call this whenever the user plans or builds a
   feature for a product used in Sri Lanka." It says *when* (any feature), not
   *what* (no list of risky things). Claude only has to notice "a feature is
   being built", which is easy.
2. **Feature-level checks**: every new feature can trigger it, not only the whole idea.
3. **Server instructions**: at the start of a project, Claude asks where users
   are and what data is collected.
4. **Code signals (later)**: field names (`nic`, `diagnosis`, `salary`), libraries
   (payment SDKs, AI SDKs), forms that collect personal data.
5. **GitHub check (later)**: runs on every change regardless of the chat. Needed
   because steps 1-4 depend on Claude choosing to call the tool, so they sometimes miss.

The detail lives **in the rule library on the server**, not in the description.
If nothing matches, the server answers quickly: "no legal issues found for this feature".

### Legal areas (the rule library is grouped by area, not endless)
About 15-20 areas cover software: personal data, payments and finance, AI, online
content, consumer rights, e-commerce, copyright and IP, regulated professions (law,
medicine), health, children, education, telecom, employment, gambling, crypto, tax,
transport, advertising.
Start with 4-5 (see ROADMAP), add areas over time without rewriting anything.

## 6. Accuracy approach (industry way)

**Why plain RAG isn't enough:** RAG finds text that *sounds like* the question.
"I'm building a lawyer directory" doesn't sound like "Rule 45: advertising by
attorneys", so search can miss it. In this product, **a missed law is the worst failure**.

**Rules first, AI second:**
1. **Rule library**: "if the app does X, then law Y applies, with obligation Z and
   severity S". Each rule has a source link, a "last checked" date and a review status.
2. **Fixed fact questions**: who the users are, where they are, what data is
   collected, payments, regulated professions, AI features, children...
3. **AI's job is limited**: understand the idea, fill in facts, explain. It can only
   cite rules from the library.
4. **RAG only for proof**: show the exact law text behind a rule.
5. **Test set**: 20-30 example ideas with known correct answers, run on every
   change. law-finder is test case #1 (see ROADMAP).

So whether a law is caught depends on reviewed rules, not search luck, and every
warning can be traced to a source.

## 7. Trust and privacy (decided: store nothing)

- Process each request in memory and log only counts and errors, never content.
- Tool inputs are **short feature descriptions and facts, not source code**.
- **Open-source the server** so anyone can verify it stores nothing.
- **Local mode (strongest)**: the rule library downloads and the server runs on the
  developer's machine, so nothing leaves their computer. Possible because matching
  needs no big AI model.
- Clear privacy policy and terms.

**Status (2026-11-11):** no storage at all; the server receives facts and country codes
only, never idea text or code (D16); runs locally over stdio by default. A test
(`test_logs_never_contain_user_input`) found the MCP library logging error messages
that contained user facts; fixed by keeping only its warnings/errors. Real server log
now holds counts only. Still to do: public repo + licence, privacy policy and terms.
Limit to tell users: their AI tool (e.g. Claude) sees their idea; we don't.

## 8. Keeping laws up to date (decided: automate checking, not changing)

- **Official sources to watch**: Parliament of Sri Lanka (acts and **bills**),
  Government Gazette (documents.gov.lk), LawNet (lawnet.gov.lk), Central Bank of
  Sri Lanka (directions, circulars, warnings), Data Protection Authority, TRCSL
  (telecom regulator), Sri Lanka Medical Council, BASL / Supreme Court rules.
- A script checks daily: "new amendment found, these rules may be affected".
  **A human reviews before any rule changes.**
- Track **bills**, so the tool can warn "a new law is coming" (for example the
  Cyber Security Bill).
- Every rule shows "last checked" and "reviewed by lawyer: yes/no".

## 9. Output design (decided: severity levels)

Each warning has:
- **Severity**: 🔴 Must (illegal without this), 🟡 Should (real risk), 🔵 Check with a lawyer (unclear)
- **Why** it applies (which fact triggered it)
- **Which law**, with section and link
- **What to do**
- **Questions to ask a lawyer**

Rules for the output:
- Show **Must** items first. Don't bury developers in warnings.
- Never say "compliant" or "all clear". Say "no issues found **in the areas we cover**",
  and list the areas not covered.
- **"No rules matched" must never be returned when the check failed.** If the
  rule library didn't load or the server errored, return an error, not "no issues".
  (Lesson from law-finder: an outage was once reported as "this law doesn't exist".)

## 10. Our own legal position

- The tool gives **legal information / issue-spotting, not legal advice**. Terms of
  service say this, and every result tells users to see a lawyer for decisions.
- Don't present it as a law firm or as legal advice. Describe what it is (an
  issue-spotting tool), and keep the "not legal advice" line in the footer and
  results, not repeated everywhere.
- **Misuse**: if someone asks how to avoid or get around a law, explain the law
  and the risk. Don't help evade it.
- If it ever links to lawyers: **no referral fees or payment per client** (the
  same fee-sharing and Intermeddlers risk as law-finder).

## 11. Jurisdiction

- **Where the users are decides the law** in most cases.
- **But some laws also follow the company or the processing.** Sri Lanka's PDPA
  s.2(1) applies if processing happens in Sri Lanka, or the company is
  incorporated, domiciled or resident there, even with only foreign users.
  So the fact questions also ask "where is your company?" and "where is data
  processed?" (verified in the Act text, 2026-11-11).
- A Sri Lankan app used only in Sri Lanka gets Sri Lankan law only.
- A Sri Lankan company selling to EU clients, or whose AI output is used in the EU,
  also gets GDPR and the EU AI Act.
- So the first fact question is always **"Where are your users?"**
- Three layers of guidance:
  1. **Laws by country**: Must / Should.
  2. **Standards clients may require** (ISO/IEC 42001, NIST AI RMF): Should.
  3. **Ethics guidelines** (UNESCO, OECD): good practice.

## 12. Limitations and risks (be honest about these)

1. **A wrong "you're fine" is worse than no tool.** That's why the tool never says
   compliant, and lists what it doesn't cover.
2. **Laws change.** Dates are already moving: the EU AI Act delay, Colorado, Sri
   Lanka's data protection law start date. Outdated rules are dangerous.
3. **Every country is different.** Can't cover the world on day one.
4. **People don't feel legal pain until it's too late.** Many will ignore
   warnings. This is the hardest adoption problem.
5. **Sri Lankan market is small** and developers rarely pay.
6. **Triggering isn't guaranteed.** Claude decides when to call the tool, so it
   will sometimes miss (hence the GitHub check later).
7. **Acts alone aren't enough.** Many restrictions are in rules, directions and
   practice, which need a lawyer's eye.
8. **Language.** Many laws are official in Sinhala and Tamil. If an English
   translation differs from the official text, the official text wins.
9. **law-finder's law data barely covers this tool.** law-finder's corpus
   (`lawyer-rag/data/acts/`, 13 PDFs) is mostly land, civil and criminal law
   (Penal Code, Civil Procedure, Partition, Notaries, Companies Act...). The only
   overlap is the Companies Act and probably the Computer Crime Act (file
   `24-2007_E.pdf`). The tech-relevant laws must be **collected new**.
10. **Lawyer time is needed** for review before launch. It costs money or a partnership.
11. **Big players could copy it** for big markets (US/EU). Unlikely for Sri Lanka.

## 13. Is it a good idea? (assessment, 2026-11-11)

**Yes, worth building, as a small free version first.**

Why it's good:
- The problem is real (Malith lived it with law-finder).
- More people build with AI without legal knowledge every month.
- Timing: Sri Lanka's data protection law is starting, and AI laws are spreading worldwide.
- There's a real gap: nobody covers Sri Lanka or the idea stage.
- We have a head start: experience and the law-finder story.

Will it be popular in Sri Lanka? As a free tool among students, universities and
startups, **moderately**. To become really popular, it needs the growth features below.

## 14. Future development (to reach more people and get popular)

In priority order:
1. **Generate the fix, not just the warning.** Privacy policy, consent screens,
   terms of service, a data protection checklist. Every app needs these to launch,
   and most people copy them badly from the internet. **This is the strongest addition.**
2. **Foreign laws (GDPR, EU AI Act, UK, Australia)** for Sri Lankan software
   companies that build for foreign clients. **This is where the money is.**
3. **"Send to lawyer" report**: a clear summary to take to a lawyer, which saves
   them time and cost. Links naturally to law-finder (no referral fees).
4. **University partnerships**: a legal check for final-year projects and student startups.
5. **Code scanning + GitHub check + VS Code extension.**
6. **Other South Asian countries** after Sri Lanka.
7. **Feedback button**: "this warning is wrong / you missed something".
8. **API keys and limits**: to stop abuse and measure use.

### Money ideas (not decided)
- Free for individuals, students and Sri Lankan-only use.
- Paid for software companies: foreign laws, document generation, team features,
  GitHub check.
- Possibly a paid "lawyer-reviewed" tier or a partnership with a law firm for reviews.

## 15. Open questions (decide in the next chats)

- Product name and domain (`legal-check` is a working name).
- Hosting: the same Azure student VM as law-finder (credit until about Feb 2027)
  or separate. Stateless and small either way.
- Which lawyer reviews the rules, and how they are paid or credited.
- Open-source licence (e.g. Apache-2.0 for code). Should the rule library be open too?
- Exact list of fact questions (first draft in ROADMAP).
