"""Match facts against the rule library and build the report.

Deterministic: same facts in, same warnings out. No AI, nothing stored.
"""

from __future__ import annotations

from typing import Any

from .library import Library, trigger_facts

SEVERITY_ORDER = {"must": 0, "should": 1, "lawyer": 2}
SEVERITY_LABEL = {"must": "Must", "should": "Should", "lawyer": "Check with a lawyer"}
DISCLAIMER = (
    "Legal information to help you spot issues, not legal advice. "
    "Rules marked 'draft' are not yet reviewed by a lawyer. "
    "Ask a Sri Lankan lawyer before making decisions."
)


DEFAULT_DONE_CHECK = "The tool cannot verify this. Check it is really done."


class FactError(ValueError):
    """The caller sent facts (or done rule ids) the library doesn't know."""


def build_facts(
    users_in: list[str],
    facts: list[str],
    company_in: str | None = None,
    processing_in: list[str] | None = None,
) -> set[str]:
    out = {f.strip() for f in facts if f.strip()}
    out |= {f"users_in:{c.strip().upper()}" for c in users_in}
    if company_in:
        out.add(f"company_in:{company_in.strip().upper()}")
    out |= {f"processing_in:{c.strip().upper()}" for c in processing_in or []}
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
    warnings = [warning(r, facts) for r in hits if r["id"] not in done]
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
            f"{len(warnings)} issue(s) found: {counts['must']} Must, {counts['should']} Should, "
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
        "areas_covered": [f"{v['label']} ({v['gaps']})" for v in covered.values()],
        "areas_not_covered": areas.get("not_covered", []),
        "countries_not_covered": sorted(countries - jurisdictions),
        "disclaimer": DISCLAIMER,
    }
