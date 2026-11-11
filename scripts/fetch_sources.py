"""Download the law sources listed in sources/sources.yaml (ROADMAP Phase 1, Step 1).

    uv run --group sources python scripts/fetch_sources.py            # all
    uv run --group sources python scripts/fetch_sources.py lk-pdpa-2022  # some

- Files go to sources/raw/ (not in git; see .gitignore).
- What was downloaded, from where, when, and its sha256 goes to
  sources/fetched.json (in git), so we know which version a rule was checked against.
- For PDFs it prints the first lines of text, so a person can confirm the
  title and number really match the manifest. A download is NOT a verification.
- TLS errors are reported, never bypassed.
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from io import BytesIO
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "sources" / "sources.yaml"
RAW = ROOT / "sources" / "raw"
LOG = ROOT / "sources" / "fetched.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) legal-check-source-fetcher"


def first_text(data: bytes, chars: int = 500) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(data))
        text = ""
        for page in reader.pages[:3]:
            text += (page.extract_text() or "") + "\n"
            if len(text) > chars:
                break
        text = " ".join(text.split())
        return text[:chars] if text else "(no text layer - scanned PDF?)"
    except Exception as exc:  # noqa: BLE001 - report, don't crash
        return f"(could not read PDF: {exc})"


def fetch(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def main(only: list[str]) -> int:
    sources = yaml.safe_load(MANIFEST.read_text())
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    RAW.mkdir(parents=True, exist_ok=True)
    failures = 0

    for src in sources:
        sid = src["id"]
        if only and sid not in only:
            continue
        urls = [u for u in [src.get("url"), *src.get("alt_urls", [])] if u]
        if not urls:
            print(f"\n== {sid}: no URL in manifest (official copy not found yet)")
            continue
        print(f"\n== {sid}: {src['title']}")
        errors = []
        for url in urls:
            try:
                data, ctype = fetch(url)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                errors.append(f"{url} -> {exc}")
                continue
            is_pdf = data[:5] == b"%PDF-"
            if not is_pdf and "pdf" in url.lower():
                errors.append(f"{url} -> not a PDF (content-type {ctype!r})")
                continue
            ext = ".pdf" if is_pdf else ".html"
            path = RAW / f"{sid}{ext}"
            path.write_bytes(data)
            log[sid] = {
                "title": src["title"],
                "url_used": url,
                "downloaded": date.today().isoformat(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "file": str(path.relative_to(ROOT)),
            }
            print(f"   OK  {url}  ({len(data):,} bytes)")
            if is_pdf:
                print(f"   TEXT: {first_text(data)}")
            break
        else:
            failures += 1
            print("   FAILED:")
            for e in errors:
                print(f"     {e}")
        for e in errors if sid in log and errors else []:
            print(f"   (earlier URL failed: {e})")

    LOG.write_text(json.dumps(dict(sorted(log.items())), indent=2) + "\n")
    print(f"\n{failures} source(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
