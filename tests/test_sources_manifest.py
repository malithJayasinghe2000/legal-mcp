"""The sources list must stay well-formed: every rule will point back to it."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "sources" / "sources.yaml"
# Every source belongs to an area the library covers (rules/areas.yaml).
AREAS = set(yaml.safe_load((ROOT / "rules" / "areas.yaml").read_text())["covered"])


def load():
    return yaml.safe_load(MANIFEST.read_text())


def test_ids_unique():
    ids = [s["id"] for s in load()]
    assert len(ids) == len(set(ids))


def test_every_source_is_complete():
    for s in load():
        assert s.get("title"), s["id"]
        assert s.get("area") in AREAS, s["id"]
        # Either a link we can download, or a note saying how to get it.
        assert s.get("url") or s.get("manual"), s["id"]
        if s.get("url"):
            # https, except CommonLII which only serves http
            ok = s["url"].startswith(("https://", "http://www.commonlii.org/"))
            assert ok, s["id"]
