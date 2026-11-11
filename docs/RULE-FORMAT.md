# Rule Format

One rule = one file (YAML), grouped by area: `rules/<area>/<rule-id>.yaml`.
Rules live in git so every change has a history. Facts that triggers may use are
listed in [rules/facts.yaml](../rules/facts.yaml).

```yaml
id: lk-pdpa-special-categories
jurisdiction: LK                 # the country whose law this is
area: personal-data
title: Health, biometric and other sensitive data need extra care
severity: must                   # must | should | lawyer   (Must / Should / Check with a lawyer)

# When does this rule apply? Every item in `all` must be true.
# An item that is a list means "at least one of these".
# `any` is a shortcut for one more "at least one of" item.
triggers:
  all:
    - collects_personal_data
    - [users_in:LK, company_in:LK, processing_in:LK]
  any: [data:health, data:biometric]

why: >
  The app processes sensitive personal data covered by Sri Lankan law.
what_to_do:
  - Get explicit consent for each purpose before collecting it.
lawyer_questions:
  - Is any other legal ground in Schedule II available to us?

law:
  name: Personal Data Protection Act, No. 9 of 2022
  section: "s.56 (definition); Schedule II"
  source_id: lk-pdpa-2022        # an id in sources/sources.yaml
  source_url: https://www.parliament.lk/uploads/acts/gbills/english/6242.pdf
  quote: "exact text from the official source"

done_check: Check the notice covers every item in Schedule V.   # optional
in_force: false                  # false = "coming law" (bill, or Act not started yet)
starts_on: 2027-01-01            # null if no start date set yet
last_checked: 2026-11-11
review_status: draft             # draft | checked_by_owner | lawyer_reviewed
reviewed_by: null
notes: ""
```

Rules for writing rules:
- `quote` is copied from the official text, never paraphrased. Dashes may be
  written as "-" (the site never shows the long dash); everything else is exact.
  `tests/test_rules.py` checks every quote really appears in the downloaded source.
  For a scanned PDF (no text), it uses a typed copy in `sources/transcripts/<source_id>.txt`.
- `source_id` must exist in `sources/sources.yaml`, and `source_url` must be that
  source's official `url` (brief D14). Quote the law **as amended**: if an
  amendment replaced the section, quote the amending Act and say so in `section`.
- Every rule has a `last_checked` date.
- `done_check` (optional) is the reminder shown when a user marks the warning as done
  (tool input `done`). The tool never verifies "done"; it lists those items separately.
- A rule with `review_status: draft` is shown to users as "not yet reviewed by a lawyer".
- Triggers use only facts from `rules/facts.yaml`, so matching stays deterministic.
- Placeholders like `<...>` are not allowed in a shipped rule (the test fails).
