"""Load and validate the rule library (rules/*.yaml, facts.yaml, areas.yaml).

Any problem raises LibraryError. The server must then report an error for every
check, never "no issues found" (CLAUDE.md: a failure is an error).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REQUIRED = (
    "id", "jurisdiction", "area", "title", "severity", "triggers", "why", "what_to_do",
    "lawyer_questions", "law", "in_force", "starts_on", "last_checked", "review_status",
)  # fmt: skip
SEVERITIES = ("must", "should", "lawyer")
REVIEW_STATUSES = ("draft", "checked_by_owner", "lawyer_reviewed")
COUNTRY_FACTS = ("users_in:", "company_in:", "processing_in:")
COUNTRY = re.compile(r"[A-Z]{2}")


class LibraryError(Exception):
    """The rule library is missing or invalid."""


@dataclass
class Library:
    rules: dict[str, dict[str, Any]]
    questions: dict[str, dict[str, str]]  # group -> fact -> question
    areas: dict[str, Any]
    facts: set[str] = field(init=False)

    def __post_init__(self) -> None:
        self.facts = {f for group in self.questions.values() for f in group}

    def is_known_fact(self, fact: str) -> bool:
        if fact in self.facts:
            return True
        prefix = next((p for p in COUNTRY_FACTS if fact.startswith(p)), None)
        return prefix is not None and COUNTRY.fullmatch(fact[len(prefix) :]) is not None


def default_rules_dir() -> Path:
    """LEGAL_CHECK_RULES_DIR, else rules shipped in the package, else the repo's rules/."""
    if env := os.environ.get("LEGAL_CHECK_RULES_DIR"):
        return Path(env)
    packaged = Path(__file__).resolve().parent / "rules"
    if packaged.is_dir():
        return packaged
    return Path(__file__).resolve().parents[2] / "rules"


def trigger_facts(triggers: dict[str, Any]) -> list[str]:
    facts: list[str] = []
    for item in triggers.get("all", []):
        facts.extend(item if isinstance(item, list) else [item])
    facts.extend(triggers.get("any", []))
    return facts


def _read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text())
    except (OSError, yaml.YAMLError) as exc:
        raise LibraryError(f"cannot read {path.name}: {exc}") from exc


def load_library(rules_dir: Path | None = None) -> Library:
    rules_dir = rules_dir or default_rules_dir()
    if not rules_dir.is_dir():
        raise LibraryError(f"rules folder not found: {rules_dir}")

    questions = _read_yaml(rules_dir / "facts.yaml")
    areas = _read_yaml(rules_dir / "areas.yaml")
    if not isinstance(questions, dict) or not isinstance(areas, dict):
        raise LibraryError("facts.yaml or areas.yaml is empty or malformed")
    library = Library(rules={}, questions=questions, areas=areas)
    covered = areas.get("covered") or {}

    problems: list[str] = []
    for path in sorted(rules_dir.glob("*/*.yaml")):
        rule = _read_yaml(path)
        name = f"{path.parent.name}/{path.name}"
        if not isinstance(rule, dict):
            problems.append(f"{name}: not a mapping")
            continue
        missing = [f for f in REQUIRED if f not in rule]
        if missing:
            problems.append(f"{name}: missing {missing}")
            continue
        if rule["id"] != path.stem or rule["area"] != path.parent.name:
            problems.append(f"{name}: id/area don't match the file path")
        if rule["area"] not in covered:
            problems.append(f"{name}: area {rule['area']!r} not in areas.yaml")
        if rule["severity"] not in SEVERITIES:
            problems.append(f"{name}: bad severity {rule['severity']!r}")
        if rule.get("duty_of", "both") not in ("controller", "processor", "both"):
            problems.append(f"{name}: bad duty_of {rule['duty_of']!r}")
        if rule["review_status"] not in REVIEW_STATUSES:
            problems.append(f"{name}: bad review_status {rule['review_status']!r}")
        facts = trigger_facts(rule["triggers"] or {})
        if not facts:
            problems.append(f"{name}: no triggers")
        unknown = [f for f in facts if not library.is_known_fact(f)]
        if unknown:
            problems.append(f"{name}: unknown facts {unknown}")
        if rule["id"] in library.rules:
            problems.append(f"{name}: duplicate id")
        library.rules[rule["id"]] = rule

    if problems:
        raise LibraryError("invalid rules: " + "; ".join(problems))
    if not library.rules:
        raise LibraryError(f"no rules found in {rules_dir}")
    return library
