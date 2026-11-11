"""Find every Act on Parliament's site that amends a law in sources/sources.yaml.

    uv run python scripts/find_amendments.py

For each main law with `parliament_name`, it searches Parliament's acts listing
(https://www.parliament.lk/en/business-of-parliament/acts-listing, the same
source law-finder uses) and lists the law and its amendments. Any Act found
that is not yet in sources.yaml is printed as MISSING, and the exit code is 1,
so a rule is never written from a law without its latest amendments.

If the main law's copy is a consolidated text (`consolidated_to: <year>`),
amendments up to that year are already inside it and shown as "in text".

It only reports. Adding a source to sources.yaml is a reviewed change (brief D9).
"""

from __future__ import annotations

import html
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "sources" / "sources.yaml"
LISTING = "https://www.parliament.lk/en/business-of-parliament/acts-listing"
UA = "legal-check source finder (checks Sri Lankan Acts for amendments)"
MAX_PAGES = 10

HEADING = re.compile(
    r"href='([^']*/act-details/([A-Z]+\d+))'\s*>\s*<h1[^>]*>([\s\S]*?)</h1>", re.IGNORECASE
)
PDF = re.compile(r"href='([^']*/uploads/acts/[^']*\.pdf)'", re.IGNORECASE)
ENDORSED = re.compile(r"Endorsed Date:\s*(\d{4}-\d{2}-\d{2})")
NUMBER_IN_TITLE = re.compile(r"No\.?\s*(\d+)\s*of\s*(\d{4})", re.IGNORECASE)


def parse_listing(page: str) -> list[dict]:
    """Acts on one listing page: number, title, endorsed date, PDF link."""
    acts = []
    matches = list(HEADING.finditer(page))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(page)
        block = page[m.start() : end]
        text = " ".join(html.unescape(re.sub(r"<[^>]*>", "", m.group(3))).split())
        split = re.match(r"^(N/A|\d+(?:\s*/\s*\d{4})?)\s*:\s*(.+)$", text, re.IGNORECASE)
        if not split:
            continue
        number = None if split.group(1).upper() == "N/A" else split.group(1).replace(" ", "")
        pdf = PDF.search(block)
        date = ENDORSED.search(block)
        acts.append(
            {
                "ref": m.group(2),
                "number": number,
                "title": split.group(2).strip(),
                "endorsed": date.group(1) if date else None,
                "pdf": urllib.parse.urljoin("https://www.parliament.lk/", pdf.group(1))
                if pdf
                else None,
            }
        )
    return acts


def search(name: str) -> list[dict]:
    found: dict[str, dict] = {}
    for page in range(1, MAX_PAGES + 1):
        query = {"keyword": name} | ({"page": str(page)} if page > 1 else {})
        url = f"{LISTING}?{urllib.parse.urlencode(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            acts = parse_listing(resp.read().decode("utf-8", errors="replace"))
        new = [a for a in acts if a["ref"] not in found]
        if not new:
            break
        found.update({a["ref"]: a for a in new})
    else:
        raise RuntimeError(f"More than {MAX_PAGES} pages for {name!r}; results may be incomplete.")
    return list(found.values())


def belongs_to(title: str, name: str) -> bool:
    """'Personal Data Protection (Amendment)' belongs to 'Personal Data Protection'."""
    t = re.sub(r"\s+", " ", title).strip().lower()
    n = name.strip().lower()
    return t == n or (t.startswith(n + " (") and t.endswith(")"))


def known_numbers(sources: list[dict]) -> set[str]:
    """'22/2025' for every source whose title says 'No. 22 of 2025'."""
    nums = set()
    for s in sources:
        for n, y in NUMBER_IN_TITLE.findall(s.get("title", "")):
            nums.add(f"{int(n)}/{y}")
    return nums


def main() -> int:
    sources = yaml.safe_load(MANIFEST.read_text())
    have = known_numbers(sources)
    missing = 0
    for src in sources:
        name = src.get("parliament_name")
        if not name:
            continue
        print(f"\n== {name}  (main law: {src['id']})")
        acts = [a for a in search(name) if belongs_to(a["title"], name)]
        if not acts:
            print("   (no Acts on Parliament's listing - e.g. a law made before 1949)")
        upto = src.get("consolidated_to")
        for a in sorted(acts, key=lambda a: a["endorsed"] or ""):
            num = a["number"] or "no number"
            year = int((a["endorsed"] or "0")[:4])
            if a["number"] in have:
                state = "ok"
            elif upto and year and year <= upto:
                state = "in text"
            else:
                state = "MISSING"
            missing += state == "MISSING"
            print(f"   [{state}] {num}  {a['title']}  endorsed {a['endorsed']}  {a['pdf']}")
    print(f"\n{missing} Act(s) missing from sources/sources.yaml.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
