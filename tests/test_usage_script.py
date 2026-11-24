"""Offline tests for scripts/usage.py: it reads the server's real usage lines."""

import asyncio
import logging
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from usage import parse, summarize  # noqa: E402

from legal_check import server  # noqa: E402

LOG = """\
2026-11-18 09:00:01,100 INFO rule library loaded: 61 rules
2026-11-18 09:00:02,200 INFO usage tool=get_fact_questions client=claude-code result=ok
2026-11-18 09:00:03,300 INFO usage tool=check_legal_risks client=claude-code result=ok facts=5 \
warnings=8 must=3 client_duties=0 done=0 areas=personal-data,telecom covered=yes
2026-11-19 10:00:00,000 INFO usage tool=check_legal_risks client=cursor result=ok facts=2 \
warnings=0 must=0 client_duties=0 done=0 areas=none covered=no
2026-11-19 10:00:01,000 INFO usage tool=check_legal_risks client=codex result=error reason=input
2026-11-01 10:00:01,000 INFO usage tool=get_checklist client=codex result=ok items=9
"""


def test_summary_counts():
    text = summarize(parse(LOG.splitlines()), days=7, today=date(2026, 11, 19))
    assert "check_legal_risks               3       1" in text
    assert "By AI tool:  claude-code 2, cursor 1, codex 1" in text
    assert "By day:      2026-11-18 2, 2026-11-19 2" in text
    assert "Top areas:   personal-data 1, telecom 1" in text
    assert "with no warnings: 1; with no Sri Lanka link: 1" in text
    assert "Errors:      input 1" in text
    assert "get_checklist" not in text  # older than 7 days


def test_empty_period_says_so():
    text = summarize([], days=7)
    assert "No usage lines found" in text


def test_reads_what_the_server_writes(caplog):
    """The script must parse the server's own lines, not just the sample above."""
    from mcp import Client

    async def run():
        async with Client(server.mcp) as client:
            await client.call_tool(
                "check_legal_risks", {"users_in": ["LK"], "facts": ["collects_personal_data"]}
            )

    caplog.set_level(logging.INFO)
    server.load()
    asyncio.run(run())
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    lines = [fmt.format(r) for r in caplog.records]
    events = parse(lines)
    assert [e["tool"] for e in events] == ["check_legal_risks"]
    assert "personal-data" in events[0]["areas"].split(",") and events[0]["covered"] == "yes"


def test_lines_from_azure_and_undated_lines():
    # Azure rows come back as "<day> <log line>"; local logs may have no date.
    lines = [
        "2026-11-19 usage tool=get_rule client=cursor result=ok area=telecom",
        "usage tool=get_rule client=codex result=ok area=telecom",
    ]
    events = parse(lines)
    assert [e["day"] for e in events] == ["2026-11-19", "undated"]
    assert "get_rule                        2" in summarize(events, 7, date(2026, 11, 19))


def test_sessions_split_real_work_from_robots():
    from usage import sessions

    lines = [
        # a person: fact list, then a check 2 minutes later
        "2026-11-19 18:06:00 usage tool=get_fact_questions client=claude-code result=ok",
        "2026-11-19 18:08:00 usage tool=check_legal_risks client=claude-code result=ok",
        # robots: fact list or prompts only, hours apart
        "2026-11-20 09:01:00 usage tool=get_fact_questions client=other result=ok",
        "2026-11-20 16:30:00 usage tool=prompt_pdpa_checklist client=other result=ok",
        "2026-11-20 16:30:05 usage tool=prompt_check_project client=other result=ok",
        "2026-11-21 10:03:00 usage tool=get_fact_questions client=other result=ok",
        # no time: left out
        "usage tool=get_fact_questions client=other result=ok",
    ]
    events = parse(lines)
    assert sessions(events) == (1, 3)
    text = summarize(events, 7, date(2026, 11, 21))
    assert "Sessions:    1 with a check or checklist; 3 only looked" in text
