"""Offline tests for the Parliament acts-listing parser (no network)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from find_amendments import belongs_to, known_numbers, parse_listing  # noqa: E402

PAGE = """
<a href='https://www.parliament.lk/en/business-of-parliament/act-details/G6384'>
  <h1 class='x'>22/2025 : Personal Data Protection (Amendment)</h1></a>
  <p>Endorsed Date: 2025-10-30</p>
  <a href='/uploads/acts/gbills/english/6384.pdf'>Download Act</a>
<a href='https://www.parliament.lk/en/business-of-parliament/act-details/P10'>
  <h1>N/A : Medical (Amendment)</h1></a>
  <p>Endorsed Date: 1949-03-15</p>
"""


def test_parse_listing():
    acts = parse_listing(PAGE)
    assert [a["ref"] for a in acts] == ["G6384", "P10"]
    first = acts[0]
    assert first["number"] == "22/2025"
    assert first["title"] == "Personal Data Protection (Amendment)"
    assert first["endorsed"] == "2025-10-30"
    assert first["pdf"] == "https://www.parliament.lk/uploads/acts/gbills/english/6384.pdf"
    # An entry with no PDF and no number is still listed, so it can't be missed.
    assert acts[1]["number"] is None and acts[1]["pdf"] is None


def test_belongs_to():
    assert belongs_to("Personal Data Protection (Amendment)", "Personal Data Protection")
    assert belongs_to("Personal Data Protection", "Personal Data Protection")
    assert not belongs_to("Medical Wastes (Management)", "Medical")
    assert not belongs_to("Payment of Gratuity", "Payment")


def test_known_numbers():
    assert known_numbers([{"title": "Online Safety Act, No. 9 of 2024"}]) == {"9/2024"}
