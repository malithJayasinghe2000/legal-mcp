"""The sources list must stay well-formed: every rule will point back to it."""

from pathlib import Path

import yaml

MANIFEST = Path(__file__).resolve().parent.parent / "sources" / "sources.yaml"
AREAS = {"personal-data", "payments", "ai", "online-content", "regulated-professions"}


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
            assert s["url"].startswith("https://"), s["id"]
