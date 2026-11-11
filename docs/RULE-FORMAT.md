# Rule Format (first draft)

One rule = one file (YAML), grouped by area: `rules/<area>/<rule-id>.yaml`.
Rules live in git so every change has a history.

```yaml
id: lk-pdpa-sensitive-health
jurisdiction: LK                 # where the USERS are, not the company
area: personal-data
title: Health data is a special category of personal data
severity: must                   # must | should | lawyer   (Must / Should / Check with a lawyer)

# When does this rule apply? All of `all` must be true, and at least one of `any`.
triggers:
  all: [users_in:LK, collects_personal_data]
  any: [data:health, data:medical_history]

why: >
  The app stores health information about people in Sri Lanka.
what_to_do:
  - Get clear consent before collecting health data.
  - Limit who can see it, and encrypt it.
lawyer_questions:
  - Do we need to register as a controller with the Data Protection Authority?

law:
  name: Personal Data Protection Act No. 9 of 2022
  section: "<section number - fill from the official text>"
  source_url: "<official link>"
  quote: "<exact text from the official source>"

last_checked: 2026-11-11
review_status: draft             # draft | checked_by_owner | lawyer_reviewed
reviewed_by: null
in_force: true                   # false for bills: shown as "coming law"
notes: ""
```

Rules for writing rules:
- `quote` must be copied from the official text, never paraphrased into it.
- Every rule has a `source_url` and a `last_checked` date.
- A rule with `review_status: draft` is shown to users as "not yet reviewed by a lawyer".
- Triggers use only facts from the fact-question list, so matching stays deterministic.
- The `<...>` values above are placeholders. Don't ship a rule that still has one.
