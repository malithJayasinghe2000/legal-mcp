"""Checker, server tools and the test set (tests/cases.yaml)."""

import asyncio
from pathlib import Path

import pytest
import yaml

from legal_check import server
from legal_check.checker import FactError, build_facts, check
from legal_check.library import load_library

CASES = yaml.safe_load((Path(__file__).parent / "cases.yaml").read_text())
LIB = load_library()


def call(tool, **args):
    """Call a tool through a real in-memory MCP client, as Claude Code would."""
    from mcp import Client

    async def run():
        async with Client(server.mcp) as client:
            return await client.call_tool(tool, args)

    return asyncio.run(run())


@pytest.fixture(autouse=True)
def loaded_server():
    server.load()
    yield
    server.load()


@pytest.mark.parametrize("case", CASES, ids=[c["name"].split()[0] for c in CASES])
def test_case(case):
    if case.get("pending"):
        pytest.xfail(case["pending"])
    facts = build_facts(case["users_in"], case["facts"], case.get("company_in"),
                        case.get("processing_in"))  # fmt: skip
    result = check(LIB, facts)
    ids = [w["rule_id"] for w in result["warnings"]]
    assert [r for r in case.get("must_include", []) if r not in ids] == []
    assert [r for r in case.get("must_exclude", []) if r in ids] == []
    not_covered = result["areas_not_covered"]
    assert [a for a in case.get("not_covered_includes", []) if a not in not_covered] == []
    if "countries_not_covered" in case:
        assert result["countries_not_covered"] == sorted(case["countries_not_covered"])
    if "max_warnings" in case:
        assert len(ids) <= case["max_warnings"], ids


def test_must_first():
    facts = build_facts(["LK"], ["collects_personal_data", "data:health", "automated_decisions"])
    order = [w["severity"] for w in check(LIB, facts)["warnings"]]
    rank = {"Must": 0, "Should": 1, "Check with a lawyer": 2}
    assert order == sorted(order, key=rank.get)


def test_no_issues_never_says_all_clear():
    result = check(LIB, build_facts(["LK"], []))
    assert result["warnings"] == []
    assert result["summary"].startswith("No issues found in the areas we cover")
    assert "all clear" not in result["summary"].lower()
    assert result["areas_not_covered"]


def test_unknown_fact_is_an_error():
    with pytest.raises(FactError):
        check(LIB, build_facts(["LK"], ["collects_nic_number"]))


def test_tool_check_returns_warnings():
    result = call("check_legal_risks", users_in=["LK"], facts=["collects_personal_data"])
    assert not result.is_error
    assert result.structured_content["warnings"]


def test_tool_unknown_fact_is_error_result():
    result = call("check_legal_risks", users_in=["LK"], facts=["made_up_fact"])
    assert result.is_error


def test_failed_library_is_error_not_no_issues(tmp_path):
    server.load(tmp_path / "missing")
    result = call("check_legal_risks", users_in=["LK"], facts=[])
    assert result.is_error
    text = result.content[0].text
    assert "did NOT run" in text and "No issues found" not in text


def test_tool_get_rule_has_quote():
    result = call("get_rule", rule_id="lk-pdpa-scope")
    assert result.structured_content["law"]["quote"]
    assert call("get_rule", rule_id="nope").is_error


def test_no_long_dash_in_output():
    facts = build_facts(["LK"], sorted(LIB.facts - {"users:children"}))
    assert "—" not in str(check(LIB, facts))
