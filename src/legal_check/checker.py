"""Match facts against the rule library and build the report.

Deterministic: same facts in, same warnings out. No AI, nothing stored.
"""

from __future__ import annotations

import json
from typing import Any

from .library import Library, trigger_facts

SEVERITY_ORDER = {"must": 0, "should": 1, "lawyer": 2}
SEVERITY_LABEL = {"must": "Must", "should": "Should", "lawyer": "Check with a lawyer"}
DISCLAIMER = (
    "Legal information to help you spot issues, not legal advice. "
    "Rules marked 'draft' are not yet reviewed by a lawyer. "
    "Ask a Sri Lankan lawyer before making decisions."
)


FOR_CLIENT = "builds_for_client"
CLIENT_NOTE = (
    "You build or run this for a client, so these are your client's duties as the "
    "'controller' under the PDPA. Tell your client; you may help them do it."
)
DEFAULT_DONE_CHECK = "The tool cannot verify this. Check it is really done."


class FactError(ValueError):
    """The caller sent facts (or done rule ids) the library doesn't know."""


def country_codes(value: str | list[str] | None) -> list[str]:
    """Country codes from what AI clients really send: "LK", ["LK"], or JSON text
    such as '["LK"]' or '"LK"'. Anything still not a 2-letter code stays as it is,
    so the check reports it as an unknown fact (an error), never ignores it."""
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    out: list[str] = []
    for item in items:
        text = str(item).strip()
        if text[:1] in '["':
            try:
                parsed = json.loads(text)
            except ValueError:
                parsed = text.strip('"[] ')
            out += country_codes(parsed) if parsed != text else [text]
        elif text:
            out.append(text.upper())
    return out


def fact_list(value: str | list[str] | dict[str, bool] | None) -> list[str]:
    """Facts from what AI clients really send: a list, JSON text of a list, or a
    yes/no table such as {"collects_personal_data": true}. Only true facts count."""
    if value is None:
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return [value]
    if isinstance(value, dict):
        return [str(k) for k, v in value.items() if v is True]
    if isinstance(value, list):
        return [str(f) for f in value]
    return [str(value)]


def build_facts(
    users_in: str | list[str],
    facts: str | list[str] | dict[str, bool],
    company_in: str | list[str] | None = None,
    processing_in: str | list[str] | None = None,
) -> set[str]:
    out = {f.strip() for f in fact_list(facts) if f.strip()}
    out |= {f"users_in:{c}" for c in country_codes(users_in)}
    out |= {f"company_in:{c}" for c in country_codes(company_in)}
    out |= {f"processing_in:{c}" for c in country_codes(processing_in)}
    return out


def matches(triggers: dict[str, Any], facts: set[str]) -> bool:
    for item in triggers.get("all", []):
        group = item if isinstance(item, list) else [item]
        if not facts.intersection(group):
            return False
    any_of = triggers.get("any")
    return not any_of or bool(facts.intersection(any_of))


def _status(rule: dict[str, Any]) -> str:
    if rule["in_force"]:
        return "In force"
    if rule.get("starts_on"):
        return f"Coming law: starts {rule['starts_on']}"
    return "Coming law: start date not set yet"


def _review(rule: dict[str, Any]) -> str:
    return {
        "draft": "Draft - not yet reviewed by a lawyer",
        "checked_by_owner": "Checked against the law text - not yet reviewed by a lawyer",
        "lawyer_reviewed": f"Reviewed by a lawyer ({rule.get('reviewed_by') or 'name not given'})",
    }[rule["review_status"]]


def warning(rule: dict[str, Any], facts: set[str]) -> dict[str, Any]:
    law = rule["law"]
    return {
        "severity": SEVERITY_LABEL[rule["severity"]],
        "title": rule["title"],
        "rule_id": rule["id"],
        "area": rule["area"],
        "triggered_by": sorted(facts.intersection(trigger_facts(rule["triggers"]))),
        "why": " ".join(rule["why"].split()),
        "what_to_do": rule["what_to_do"],
        "lawyer_questions": rule["lawyer_questions"],
        "law": {k: law[k] for k in ("name", "section", "source_url")},
        "status": _status(rule),
        "review": _review(rule),
        "last_checked": str(rule["last_checked"]),
    }


def check(library: Library, facts: set[str], done: set[str] | None = None) -> dict[str, Any]:
    """`done`: rule ids the user says are already handled. They move to a "done"
    list (with a reminder to check them) instead of being dropped silently."""
    done = done or set()
    unknown = sorted(f for f in facts if not library.is_known_fact(f))
    if unknown:
        raise FactError(
            f"Unknown facts: {unknown}. Use only facts from get_fact_questions; "
            "an unknown fact could hide a law, so the check was not run."
        )
    unknown_done = sorted(d for d in done if d not in library.rules)
    if unknown_done:
        raise FactError(
            f"Unknown rule ids in done: {unknown_done}. Use rule_id values from a "
            "previous check_legal_risks result."
        )

    hits = [r for r in library.rules.values() if matches(r["triggers"], facts)]
    hits.sort(key=lambda r: (SEVERITY_ORDER[r["severity"]], not r["in_force"], r["id"]))
    # Building for a client: the client's (controller's) duties go to a separate
    # list, so the builder sees their own duties without losing the client's.
    for_client = FOR_CLIENT in facts
    client_hits = [r for r in hits if for_client and r.get("duty_of") == "controller"]
    hits = [r for r in hits if r not in client_hits]
    warnings = [warning(r, facts) for r in hits if r["id"] not in done]
    client_duties = [
        {
            "rule_id": r["id"],
            "title": r["title"],
            "severity": SEVERITY_LABEL[r["severity"]],
            "law": f"{r['law']['name']}, {r['law']['section']}",
        }
        for r in client_hits
    ]
    done_items = [
        {
            "rule_id": r["id"],
            "title": r["title"],
            "severity": SEVERITY_LABEL[r["severity"]],
            "check": " ".join((r.get("done_check") or DEFAULT_DONE_CHECK).split()),
        }
        for r in hits
        if r["id"] in done
    ]

    areas = library.areas
    covered = areas["covered"]
    jurisdictions = set(areas.get("jurisdictions_covered", []))
    countries = {f.split(":", 1)[1] for f in facts if f.split(":", 1)[0] in
                 ("users_in", "company_in", "processing_in")}  # fmt: skip
    counts = {k: sum(w["severity"] == SEVERITY_LABEL[k] for w in warnings) for k in SEVERITY_ORDER}

    if warnings:
        summary = (
            f"{len(warnings)} {'issue' if len(warnings) == 1 else 'issues'} found: "
            f"{counts['must']} Must, {counts['should']} Should, "
            f"{counts['lawyer']} Check with a lawyer. Must items are listed first."
        )
    elif done_items:
        summary = (
            "No open issues in the areas we cover, apart from items you marked done "
            "(not verified by this tool). This does not mean the product is compliant: "
            "see the areas and countries not covered."
        )
    else:
        summary = (
            "No issues found in the areas we cover. This does not mean the product is "
            "compliant: see the areas and countries not covered."
        )
    if client_duties:
        summary += (
            f" {len(client_duties)} more item(s) are your client's duties, listed under "
            "'client_duties'."
        )
    if done_items:
        summary += f" {len(done_items)} item(s) marked done by you are listed under 'done'."
    if not countries & jurisdictions:
        summary += (
            " None of the given countries are covered (this tool covers Sri Lankan law only)."
        )

    return {
        "summary": summary,
        "warnings": warnings,
        "done": done_items,
        "client_duties": {"note": CLIENT_NOTE, "items": client_duties} if client_duties else None,
        "areas_covered": [f"{v['label']} ({v['gaps']})" for v in covered.values()],
        "areas_not_covered": areas.get("not_covered", []),
        "countries_not_covered": sorted(countries - jurisdictions),
        "disclaimer": DISCLAIMER,
    }


# Checklists: the rules of one law that apply to the product, each with what to look for
# in the code (`checklist.look_for`) or ask the user (`checklist.ask`). The AI marks each
# item Found / Missing / Can't tell from code. Never a score, never "compliant".
CHECKLISTS = {
    "pdpa": {
        "name": "PDPA 2027 checklist",
        "law": "Personal Data Protection Act, No. 9 of 2022 (as amended by No. 22 of 2025)",
        "source_prefix": "lk-pdpa",
        "start_source": "Gazette No. 2498/16",
    },
}

CHECKLIST_HOW = (
    "For each item, look in the code for `look_for` and mark it: Found (give the file, line "
    "and a short code excerpt; no evidence means not Found), Missing, or Can't tell from "
    "code (then put the `ask` question to the user). Report 'X of Y found in your code', "
    "never a score or a percentage, and never say compliant or ready. Found means seen in "
    "the code, not verified."
)


def checklist(library: Library, facts: set[str], law: str = "pdpa") -> dict[str, Any]:
    spec = CHECKLISTS.get(law)
    if spec is None:
        raise FactError(f"Unknown checklist {law!r}. Available: {sorted(CHECKLISTS)}.")
    result = check(library, facts)  # same fact checks, country rules and client split
    client_ids = {i["rule_id"] for i in (result["client_duties"] or {}).get("items", [])}
    applies = {w["rule_id"] for w in result["warnings"]} | client_ids

    def item(rule: dict[str, Any]) -> dict[str, Any]:
        hint = rule["checklist"]
        return {
            "rule_id": rule["id"],
            "title": rule["title"],
            "severity": SEVERITY_LABEL[rule["severity"]],
            "law": f"{rule['law']['name']}, {rule['law']['section']}",
            "status": _status(rule),
            "look_for": hint.get("look_for"),
            "ask": hint.get("ask"),
        }

    rules = [
        r
        for r in library.rules.values()
        if r["id"] in applies
        and r["law"]["source_id"].startswith(spec["source_prefix"])
        and r.get("checklist")
    ]
    rules.sort(key=lambda r: (SEVERITY_ORDER[r["severity"]], r["id"]))
    items = [item(r) for r in rules if r["id"] not in client_ids]
    client_items = [item(r) for r in rules if r["id"] in client_ids]

    dates = sorted({r["starts_on"] for r in rules if not r["in_force"] and r["starts_on"]})
    undated = sum(1 for r in rules if not r["in_force"] and not r["starts_on"])
    starts = None
    if dates:
        d = dates[0]
        starts = f"{d.year} ({d.day} {d:%B %Y}, {spec['start_source']})"
    if not items and not client_items:
        summary = (
            f"No {spec['name']} items apply to these facts. This is not a statement that the "
            "product is compliant."
        )
        if result["countries_not_covered"] and not applies:
            summary += " " + result["summary"]
    else:
        summary = (
            f"{len(items)} item(s) on your {spec['name']}"
            + (f", plus {len(client_items)} that are your client's duties" if client_items else "")
            + "."
        )
    last = max(str(r["last_checked"]) for r in library.rules.values())
    return {
        "checklist": spec["name"],
        "law": spec["law"],
        "summary": summary,
        "starts": starts,
        "items_without_start_date": undated,
        "rules_version": f"Rulewise rules checked up to {last}",
        "how_to_report": CHECKLIST_HOW,
        "items": items,
        "client_items": client_items,
        "disclaimer": DISCLAIMER,
    }
