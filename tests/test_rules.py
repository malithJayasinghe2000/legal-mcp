"""Every rule must be complete, use only known facts, and quote its source exactly.

The quote check reads the downloaded sources (sources/raw/, not in git). If a
source isn't downloaded, that test is skipped with a message; run
`uv run --group sources python scripts/fetch_sources.py` first.
"""

import datetime
import re
import unicodedata
from functools import cache
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
RAW = ROOT / "sources" / "raw"

REQUIRED = [
    "id", "jurisdiction", "area", "title", "severity", "triggers", "why", "what_to_do",
    "lawyer_questions", "law", "in_force", "starts_on", "last_checked", "review_status",
    "reviewed_by", "notes",
]  # fmt: skip
SEVERITIES = {"must", "should", "lawyer"}
REVIEW = {"draft", "checked_by_owner", "lawyer_reviewed"}
COUNTRY_FACTS = ("users_in:", "company_in:", "processing_in:")


def rule_files():
    return sorted(p for p in RULES_DIR.rglob("*.yaml") if p.name != "facts.yaml")


RULES = {p: yaml.safe_load(p.read_text()) for p in rule_files()}
SOURCES = {s["id"]: s for s in yaml.safe_load((ROOT / "sources" / "sources.yaml").read_text())}
FACTS = {
    fact
    for group in yaml.safe_load((RULES_DIR / "facts.yaml").read_text()).values()
    for fact in group
}


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def trigger_facts(triggers):
    for item in triggers.get("all", []):
        yield from item if isinstance(item, list) else [item]
    yield from triggers.get("any", [])


def known_fact(fact: str) -> bool:
    if fact in FACTS:
        return True
    prefix = next((p for p in COUNTRY_FACTS if fact.startswith(p)), None)
    return bool(prefix) and re.fullmatch(r"[A-Z]{2}", fact[len(prefix) :]) is not None


def normalise(text: str) -> str:
    """Compare law text ignoring PDF spacing, ligatures, dash and quote styles."""
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[‐-―−]", "-", text)
    text = re.sub(r"[“”„‟]", '"', text)
    text = re.sub(r"[‘’‚‛]", "'", text)
    return re.sub(r"\s+", "", text)


@cache
def source_text(source_id: str) -> str | None:
    # A scanned PDF has no text layer: use its typed transcript (in git) instead.
    transcript = ROOT / "sources" / "transcripts" / f"{source_id}.txt"
    if transcript.exists():
        return normalise(transcript.read_text())
    pdf = RAW / f"{source_id}.pdf"
    if not pdf.exists():
        return None
    from pypdf import PdfReader

    return normalise("\n".join(p.extract_text() or "" for p in PdfReader(pdf).pages))


def test_there_are_rules():
    assert RULES, "no rules found"


@pytest.mark.parametrize("path", rule_files(), ids=lambda p: p.stem)
def test_rule_is_complete(path):
    r = RULES[path]
    assert [f for f in REQUIRED if f not in r] == []
    assert r["id"] == path.stem
    assert r["area"] == path.parent.name
    assert r["severity"] in SEVERITIES
    assert r["review_status"] in REVIEW
    assert isinstance(r["in_force"], bool)
    assert r["starts_on"] is None or isinstance(r["starts_on"], datetime.date)
    assert isinstance(r["last_checked"], datetime.date)
    assert r["what_to_do"], "a rule must say what to do"
    for s in strings(r):
        assert "<" not in s and ">" not in s, f"placeholder left: {s[:60]!r}"
        assert "—" not in s, "use '-' not the long dash"


@pytest.mark.parametrize("path", rule_files(), ids=lambda p: p.stem)
def test_triggers_use_known_facts(path):
    facts = list(trigger_facts(RULES[path]["triggers"]))
    assert facts, "a rule needs at least one trigger"
    assert [f for f in facts if not known_fact(f)] == []


@pytest.mark.parametrize("path", rule_files(), ids=lambda p: p.stem)
def test_source_is_official(path):
    law = RULES[path]["law"]
    src = SOURCES.get(law["source_id"])
    assert src, f"unknown source_id {law['source_id']}"
    assert law["source_url"] == src["url"], "source_url must be the official url in sources.yaml"


@pytest.mark.parametrize("path", rule_files(), ids=lambda p: p.stem)
def test_quote_is_in_source(path):
    law = RULES[path]["law"]
    text = source_text(law["source_id"])
    if text is None:
        pytest.skip(f"{law['source_id']} not downloaded (run scripts/fetch_sources.py)")
    assert normalise(law["quote"]) in text, "quote not found word for word in the source"
