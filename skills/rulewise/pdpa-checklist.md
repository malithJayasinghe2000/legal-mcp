# Rulewise PDPA 2027 checklist

Check how ready a project's code is for Sri Lanka's Personal Data Protection Act (PDPA) and
write a checklist file. Use this when the user asks for the PDPA checklist, or whether their
project is ready for the PDPA or Sri Lanka's data protection law.

The checklist items come only from the Rulewise MCP tools. Never add items or laws of your
own, never give a score or a percentage, and never say the project is "compliant" or "ready".

## 1. Find where the users and the company are
Look for clear signs in the project: the README ("for Sri Lanka"), prices in LKR, +94 phone
numbers, Sri Lankan payment gateways such as PayHere, `.lk` domains. If the files clearly say,
use that and name the file. If not, ask one short question: "Rulewise checks Sri Lankan law.
Will your users or your company be in Sri Lanka?" Never guess.

## 2. Read the project
Read what shows how personal data is handled: README and docs, dependency files, database
schemas and models, sign-up and other forms, API routes, auth code, privacy or terms pages,
scheduled jobs, and messaging code (SMS, email, push). Skip `node_modules`, build output and
vendored code. Never open secret files (`.env`, keys, credentials) and never copy a secret.

## 3. Choose the facts
Call `get_fact_questions` once. Pick only the facts the project shows, with evidence (file and
line). Use `builds_for_client` only for an agency or outsourcing project built for one client
who decides how the data is used. Your own product is not that, even if businesses pay to use
it (a SaaS, a platform for firms). If you are not sure, ask the user.

## 4. Get the checklist
Call `get_checklist` with the facts, the country codes and `law: "pdpa"`. Send only facts and
country codes, never code or file names. If the tool returns an error, tell the user the check
failed and write no file. If it returns no items, say so with its summary; that is not
"compliant".

## 5. Check each item in the code
`look_for` is a list of parts, and every part is required. For each item in `items`, look in
the code for each part, then mark the item:
- **Found:** every part is seen in the code. Give the file and line and a short excerpt (one
  line) for each part. No evidence means not seen. "Probably exists somewhere" is not seen.
  A part is seen only if the code actually does it: a database column, setting or field that
  no code fills or reads does not count.
- **Missing:** one or more parts are not seen, even if others are. Write "Seen:" with the
  parts that are there (file and line) and "Not seen:" with the parts that are not, for
  example "Seen: passwords hashed (`lib/auth.ts:2`). Not seen: HTTPS only, encrypted fields,
  access control, access logs."
- **Can't tell from code:** only when the item has no `look_for`. Put the item's `ask`
  question to the user.
Mark every item by these rules alone, so the same code gets the same result in any tool.
If an item has both `look_for` and `ask`, mark it from the code and also list the `ask`
question under "Please confirm".

Count: X = items Found, Y = all items in `items`, Z = items you could not tell from code.
`client_items` are your client's duties: list them separately and leave them out of the count.

## 6. Write `RULEWISE-PDPA-CHECKLIST.md` at the project root
Replace an earlier Rulewise checklist. Ask before overwriting any other file. Layout:

```markdown
# PDPA 2027 checklist: X of Y found in your code (Z can't tell from code)

Most of the PDPA starts in <starts, from the tool>. <items_without_start_date> item(s) have no start date yet.
<rules_version, from the tool> | Checked on <YYYY-MM-DD> | Project: <name>

Found in code, not verified. Legal information, not legal advice. The rules are drafts, not
yet reviewed by a lawyer. Ask a Sri Lankan lawyer before you rely on this checklist.

## Top 3 to fix
1. <a Missing Must item, one line, with the file>

## Checklist
| | Item | Severity | In your code | Law |
|---|---|---|---|---|
| ✔ | <title> | Must | `<file>:<line>` `<short excerpt>` | <law and section> |
| ✘ | <title> | Must | Seen: <parts, file:line>. Not seen: <parts> | <law and section> |
| ? | <title> | Must | Can't tell from code | <law and section> |

## Please confirm
- <each ask question>

## Your client's duties
<only if client_items: title and law for each>

## Not yet in force
<items whose status says "start date not set yet", if any: they are on the list, but have no start date>

---
Run again after your fixes: ask "run the Rulewise PDPA checklist".
```

- Use the headline exactly as above, with X, Y and Z filled in. Leave out the "no start date"
  sentence when `items_without_start_date` is 0.
- "Top 3 to fix" lists only items marked Missing (✘): Missing Must items first, then Missing
  Should items. Never put a "Can't tell from code" item there; it goes under "Please confirm".
  If nothing is Missing, write "Nothing missing was found in the code" and still list the
  Please confirm questions.
- Never write a score, a percentage, "compliant", "ready" or "100%".

## 7. Tell the user
In the chat: the headline, the start line, the top 3 to fix (Missing items only), the "Can't
tell from code" items as questions, and the file path. Don't change the
code in this step; offer to help fix the Missing items next.
