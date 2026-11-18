"""The Rulewise skill (skills/rulewise/SKILL.md) must stay valid and in step with the server."""

import asyncio
import re
from pathlib import Path

import yaml

from legal_check import server

SKILL = Path(__file__).resolve().parent.parent / "skills" / "rulewise" / "SKILL.md"


def frontmatter_and_body() -> tuple[dict, str]:
    text = SKILL.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    assert match, "SKILL.md must start with --- frontmatter ---"
    return yaml.safe_load(match.group(1)), match.group(2)


def server_tool_names() -> set[str]:
    from mcp import Client

    async def run():
        async with Client(server.mcp) as client:
            return {t.name for t in (await client.list_tools()).tools}

    return asyncio.run(run())


def test_skill_frontmatter():
    meta, _ = frontmatter_and_body()
    assert meta["name"] == SKILL.parent.name == "rulewise"
    assert re.fullmatch(r"[a-z0-9-]{1,64}", meta["name"])
    assert 0 < len(meta["description"]) <= 1024


def test_skill_names_only_real_tools():
    _, body = frontmatter_and_body()
    named = set(re.findall(r"`((?:get|check)_[a-z_]+)`", body))
    assert named, "the skill should name the Rulewise tools"
    assert named <= server_tool_names()


def test_skill_keeps_the_safety_rules():
    _, body = frontmatter_and_body()
    for must_say in ["never guessed", "compliant", "check failed", "not yet reviewed by a lawyer"]:
        assert must_say in body, f"skill lost the rule: {must_say!r}"
    assert "—" not in body, "use '-' not the long dash"
