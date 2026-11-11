"""Website JSON API: same checker, errors are errors, nothing echoed into logs."""

import logging

import pytest
from starlette.testclient import TestClient

from legal_check import server, web_api  # noqa: F401  (registers routes)


@pytest.fixture
def client():
    server.load()
    with TestClient(server.mcp.streamable_http_app()) as c:
        yield c
    server.load()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["rules"] > 30


def test_questions(client):
    data = client.get("/api/questions").json()
    assert data["questionnaire"]["sections"][0]["id"] == "where"
    assert data["areas"]["not_covered"]


def test_check_matches_mcp_checker(client):
    body = {"users_in": ["LK"], "facts": ["collects_personal_data", "data:health"]}
    r = client.post("/api/check", json=body)
    assert r.status_code == 200
    ids = [w["rule_id"] for w in r.json()["warnings"]]
    assert "lk-pdpa-special-categories" in ids
    assert r.headers["cache-control"] == "no-store"


def test_unknown_fact_is_400_not_empty_result(client):
    r = client.post("/api/check", json={"users_in": ["LK"], "facts": ["nope"]})
    assert r.status_code == 400 and "did not run" in r.json()["error"]


@pytest.mark.parametrize(
    "body", [{"facts": []}, {"users_in": "LK"}, {"users_in": ["LK"], "facts": [1]}, [1, 2]]
)
def test_bad_input_is_400(client, body):
    assert client.post("/api/check", json=body).status_code == 400


def test_too_large_is_413(client):
    r = client.post("/api/check", content=b"x" * 30_000)
    assert r.status_code == 413


def test_library_failure_is_503(client, tmp_path):
    server.load(tmp_path / "missing")
    r = client.post("/api/check", json={"users_in": ["LK"], "facts": []})
    assert r.status_code == 503 and "did NOT run" in r.json()["error"]


def test_rule_detail_has_quote(client):
    assert client.get("/api/rules/lk-pdpa-scope").json()["law"]["quote"]
    assert client.get("/api/rules/nope").status_code == 404


def test_api_logs_hold_no_input(client, caplog):
    caplog.set_level(logging.DEBUG)
    client.post("/api/check", json={"users_in": ["MV"], "facts": ["data:health", "zzsecret"]})
    client.post("/api/check", json={"users_in": ["MV"], "facts": ["data:health"]})
    logged = "\n".join(r.getMessage() for r in caplog.records)
    assert "zzsecret" not in logged and "data:health" not in logged and "MV" not in logged
