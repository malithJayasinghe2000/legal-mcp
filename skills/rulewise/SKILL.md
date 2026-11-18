---
name: rulewise
description: Spot legal issues before building. Use whenever the user plans, designs or builds a product or feature (app, website, API, online service) that may have users or a company in Sri Lanka, or where the country is not known yet - for example collecting personal data, payments, AI features, messaging or SMS, user content, payroll, or doctors and lawyers. Checks Sri Lankan law with the Rulewise MCP tools. Legal information, not legal advice.
license: MIT
---

# Rulewise

Rulewise warns which laws apply to what the user is building, starting with Sri Lankan law.
The law comes only from the Rulewise MCP tools (`get_fact_questions`, `check_legal_risks`,
`get_rule`). Never add laws of your own.

## When to use
Before planning or writing code for a product or feature: a new app, a new feature, a data
field, a payment flow, an AI feature, messages to users. Not for pure styling or refactoring.

## Steps
1. **Country first, never guessed.** If the user hasn't said where the users and the company
   are, ask one short question: "Rulewise checks Sri Lankan law. Will your users or your
   company be in Sri Lanka?" If neither is in Sri Lanka, say Rulewise does not cover that
   country yet. Never say "no issues" then.
2. Call `get_fact_questions` once to learn the facts you may send.
3. Call `check_legal_risks` with the facts that are true for this feature and the country
   codes. Send only facts and country codes, never the user's idea text or code.
4. Explain the result before building:
   - **Must** items first, then Should, then Check with a lawyer, each with the law and section.
   - Change the plan or code to handle the Must items, or ask the user if it is a business decision.
   - Never say "compliant" or "all clear". Say "no issues found in the areas Rulewise covers"
     and list the areas not covered.
   - Say the rules are drafts, not yet reviewed by a lawyer.
5. When the user says a warning is handled, pass its rule id in `done` on later checks. Done
   items are not verified: remind the user to check them.
6. Check again when a later feature adds new facts (new data, payments, AI, messages).

## Errors and limits
- If the tool returns an error, say the check failed. It is never "no issues found".
- If the Rulewise tools are not available, tell the user to add the MCP server
  (https://legal-mcp.vercel.app shows how) and don't guess the law.
- If the user asks how to get around a law, explain the law and the risk instead.
