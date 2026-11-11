"""The website's guided questions must be able to reach every fact (else a law is unreachable)."""

from pathlib import Path

import yaml

RULES = Path(__file__).resolve().parent.parent / "rules"
FACTS = yaml.safe_load((RULES / "facts.yaml").read_text())
FLOW = yaml.safe_load((RULES / "questionnaire.yaml").read_text())


def asked_facts() -> list[str]:
    out = []
    for section in FLOW["sections"]:
        for q in section["questions"]:
            if q["kind"] == "country":
                continue
            if q["kind"] == "yesno":
                out.append(q.get("fact", q["id"]))
            else:
                out.extend(o["fact"] for o in q["options"])
    return out


def test_every_fact_is_asked_exactly_once():
    expected = {f for group, facts in FACTS.items() if group != "where" for f in facts}
    asked = asked_facts()
    assert sorted(set(asked)) == sorted(expected), "missing or unknown facts"
    assert len(asked) == len(set(asked)), "a fact is asked twice"


def test_country_questions_cover_where():
    countries = {
        q["id"] for s in FLOW["sections"] for q in s["questions"] if q["kind"] == "country"
    }
    assert countries == {"users_in", "company_in", "processing_in"}


def test_show_if_points_to_asked_facts():
    asked = set(asked_facts())
    for s in FLOW["sections"]:
        for q in s["questions"]:
            for dep in [q.get("show_if"), *q.get("show_if_any", [])]:
                assert dep is None or dep in asked, f"{q['id']}: show_if {dep!r}"


def test_no_long_dash_in_questions():
    assert "—" not in (RULES / "questionnaire.yaml").read_text()
