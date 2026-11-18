# Rulewise project check

Check a whole existing project with Rulewise and write a report file. Use this when the user
asks to check their project, codebase or app with Rulewise, or asks for a Rulewise report.

The law comes only from the Rulewise MCP tools. Never add laws of your own. Your job is to
read the project, find the facts, run the check and explain the result.

## 1. Find where the users and the company are
Look for clear signs in the project: the README or docs ("for Sri Lanka"), prices in LKR,
+94 phone numbers, Sri Lankan payment gateways such as PayHere, `.lk` domains.
- If the files clearly say, use that and name the file you found it in.
- If not, ask one short question: "Rulewise checks Sri Lankan law. Will your users or your
  company be in Sri Lanka?" Never guess.
- If neither is in Sri Lanka, say Rulewise does not cover that country yet and stop. Never
  say "no issues" then.

## 2. Read the project for facts
Read what shows what the product does, not every file:
- README, docs and product notes
- dependency files (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `pom.xml`,
  `Gemfile`...): payment, AI, SMS, email, analytics and cloud SDKs
- database schemas, migrations and models: what personal data is kept (NIC, health, location,
  financial, dates of birth or ages)
- API routes, forms and screens: sign-up, payments, uploads, chat, posts, messages
- config that names services or cloud regions

Skip `node_modules`, build output and vendored code. Never open secret files (`.env`, keys,
credentials) and never copy a secret into the report.

## 3. Choose the facts
Call `get_fact_questions` once. Pick only the facts the project shows, and for each one note
the evidence: the file path and line, field or function, for example
`db/schema.sql:14 (patients.nic)`.
- If a fact is likely but not clear from the code, ask the user in one short list (at most 5
  questions), or leave it out and list it under "Assumptions".
- If the project is built for a client who decides how the data is used, use
  `builds_for_client`.

## 4. Run the check
Call `check_legal_risks` with the facts and country codes only. Never send code, file
contents or file names to Rulewise.
If the tool returns an error, tell the user the check failed and do not write a report. A
failed check is never "no issues found".

## 5. Write `RULEWISE-REPORT.md` at the project root
Replace an earlier Rulewise report. Ask before overwriting any other file. Use this layout and
fill it only from what the tool returned, plus your evidence for each fact:

```markdown
# Rulewise report - <project name>

Date: <YYYY-MM-DD> | Users in: <codes> | Company in: <code>

Legal information, not legal advice. The rules are drafts, not yet reviewed by a lawyer.
Ask a Sri Lankan lawyer before making decisions.

## Summary
<n> Must, <n> Should, <n> Check with a lawyer.
Fix first: <up to 3 Must items, one line each, with the file they apply to>

## Must
### <title>
- Law: <law name>, <section> - <source link>
- Why: <why, in one sentence>
- In your code: `<file>:<line>` - <what is there>
- What to do:
  - <each what_to_do item>

## Should
<same layout>

## Check with a lawyer
<same layout>

## Your client's duties
<only if the result has client duties: title, law and section for each>

## Already handled (not verified)
<only if the result has done items>

## Questions for a lawyer
1. <every lawyer question from the warnings, without repeats>

## Facts used
| Fact | Evidence in the code |
|---|---|
| <fact> | `<file>:<line>` |

## Assumptions
<facts you assumed or left out because the code did not show them>

## Not covered by Rulewise
<areas_not_covered and countries_not_covered from the result, copied exactly>

---
Re-run this check after big changes: ask "check my project with Rulewise".
```

- Must items first. Link each warning to the code by its `triggered_by` facts and your evidence.
- "Fix first" picks the Must items that are in force now and clearly shown in the code (for
  example an AI prompt, a database field or a fee), not the general duties every app has.
- Write nothing about the law that the tool did not return: no extra laws, no extra "not
  covered" areas, no guesses about how the result would change. Put open points under
  "Assumptions" as questions for the user.
- If there are no warnings, write "No issues found in the areas Rulewise covers" and still
  list what is not covered. Never write "compliant" or "all clear".
- Keep the law, section and quote exactly as the tool gave them.

## 6. Tell the user
In the chat: the counts, the Must items in one line each, and the report's path. Don't change
the code in this step; offer to help fix the Must items next. If the user asks how to get
around a law, explain the law and the risk instead.
