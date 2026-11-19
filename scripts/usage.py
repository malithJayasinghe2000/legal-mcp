"""Print Rulewise usage counts from the hosted server's log (counts only, never content).

    uv run python scripts/usage.py              # last 7 days, from Azure
    uv run python scripts/usage.py --days 30    # Azure keeps logs about 30 days
    uv run python scripts/usage.py --file x.log # from a saved log (or a local server's output)

Reads the `usage ...` lines the server writes (src/legal_check/usage.py). Azure access uses
the same Docker az CLI and login as scripts/deploy_azure.sh. Counts calls, not people:
there are no user ids or IP addresses, by design (brief D6).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

APP = "rulewise"
GROUP = "rulewise"
AZ = ["docker", "run", "--rm", "-e", "AZURE_EXTENSION_USE_DYNAMIC_INSTALL=yes_without_prompt",
      "-v", f"{Path.home()}/.azure:/root/.azure", "mcr.microsoft.com/azure-cli", "az"]  # fmt: skip
# "2026-11-19 10:00:00,123 INFO usage tool=..." (the date is missing in older server logs)
LINE = re.compile(r"^(?:(?P<day>\d{4}-\d{2}-\d{2})\S*\s.*?)?\busage (?P<rest>tool=.*)")


def parse(lines: list[str]) -> list[dict[str, str]]:
    """Usage lines -> list of {day, tool, client, result, ...}. Other lines are skipped."""
    events = []
    for raw in lines:
        m = LINE.search(raw)
        if not m:
            continue
        fields = dict(p.split("=", 1) for p in m["rest"].split() if "=" in p)
        events.append({"day": m["day"] or "undated", **fields})
    return events


def summarize(events: list[dict[str, str]], days: int, today: date | None = None) -> str:
    today = today or date.today()
    start = (today - timedelta(days=days - 1)).isoformat()
    events = [e for e in events if e["day"] >= start or e["day"] == "undated"]
    out = [
        f"Rulewise usage, last {days} days (hosted server only)",
        "Counts calls, not people. Nothing about users is kept.",
        "",
    ]
    if not events:
        out.append("No usage lines found in this period.")
        return "\n".join(out)

    checks = [e for e in events if e.get("tool") == "check_legal_risks" and e["result"] == "ok"]
    tools = Counter(e.get("tool", "?") for e in events)
    errors = Counter(e.get("tool", "?") for e in events if e.get("result") == "error")
    out.append("Calls by tool                 calls  errors")
    for tool, n in tools.most_common():
        out.append(f"  {tool:<27} {n:>5}  {errors[tool]:>6}")
    out.append("")
    out.append("By AI tool:  " + _join(Counter(e.get("client", "?") for e in events)))
    out.append("By day:      " + _join(Counter(e["day"] for e in events), by_key=True))
    areas = Counter(a for e in checks for a in e.get("areas", "none").split(",") if a != "none")
    out.append("Top areas:   " + (_join(areas) or "-") + "  (in checks)")
    no_country = sum(e.get("covered") == "no" for e in checks)
    nothing = sum(e.get("warnings") == "0" for e in checks)
    out.append(f"Checks with no warnings: {nothing}; with no Sri Lanka link: {no_country}")
    reasons = Counter(e.get("reason", "?") for e in events if e.get("result") == "error")
    if reasons:
        out.append("Errors:      " + _join(reasons) + "  (library = rules failed to load)")
    return "\n".join(out)


def _join(counter: Counter, by_key: bool = False) -> str:
    items = sorted(counter.items()) if by_key else counter.most_common()
    return ", ".join(f"{k} {v}" for k, v in items)


def azure_lines(days: int) -> list[str]:
    def az(*args: str) -> str:
        done = subprocess.run([*AZ, *args, "-o", "tsv"], capture_output=True, text=True)
        if done.returncode != 0:
            sys.exit(f"az {args[0]} {args[1]} failed:\n{done.stderr.strip()[-800:]}")
        return done.stdout.strip()

    env = az("containerapp", "show", "--name", APP, "--resource-group", GROUP,
             "--query", "properties.environmentId")  # fmt: skip
    customer_id = "properties.appLogsConfiguration.logAnalyticsConfiguration.customerId"
    workspace = az("containerapp", "env", "show", "--ids", env, "--query", customer_id)
    query = (
        f"ContainerAppConsoleLogs_CL | where TimeGenerated > ago({days}d) "
        '| where Log_s has "usage tool=" '
        "| project Day = format_datetime(TimeGenerated, 'yyyy-MM-dd'), Log_s"
    )
    done = subprocess.run(
        [*AZ, "monitor", "log-analytics", "query", "-w", workspace,
         "--analytics-query", query, "-o", "json"],
        capture_output=True, text=True,
    )  # fmt: skip
    if done.returncode != 0:
        sys.exit(f"Log query failed:\n{done.stderr.strip()[-800:]}")
    # Azure's own timestamp gives the day, even for lines the server wrote without a date.
    return [f"{row['Day']} {row['Log_s']}" for row in json.loads(done.stdout)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--file", help="read a saved log instead of Azure ('-' = stdin)")
    args = parser.parse_args()
    if args.file:
        text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text()
        lines = text.splitlines()
    else:
        if os.system("docker info >/dev/null 2>&1") != 0:
            sys.exit("Docker is not running. Open Docker Desktop (the az CLI runs in Docker).")
        lines = azure_lines(args.days)
    print(summarize(parse(lines), args.days))


if __name__ == "__main__":
    main()
