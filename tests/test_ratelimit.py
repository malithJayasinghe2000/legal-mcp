"""The hosted server's request limit: blocks a flood, forgets old requests, stores nothing."""

import asyncio

from legal_check.ratelimit import RateLimit


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


async def ok_app(scope, receive, send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"ok"})


def call(limit: RateLimit, ip: str, path: str = "/mcp") -> int:
    sent = []

    async def send(message):
        sent.append(message)

    scope = {"type": "http", "path": path, "headers": [(b"x-forwarded-for", ip.encode())]}
    asyncio.run(limit(scope, None, send))
    return sent[0]["status"]


def test_blocks_after_limit_then_recovers():
    clock = Clock()
    limit = RateLimit(ok_app, per_minute=3, clock=clock)
    assert [call(limit, "1.2.3.4") for _ in range(4)] == [200, 200, 200, 429]
    assert call(limit, "5.6.7.8") == 200  # other people are not affected
    clock.now = 61
    assert call(limit, "1.2.3.4") == 200


def test_health_is_never_limited():
    limit = RateLimit(ok_app, per_minute=1, clock=Clock())
    assert [call(limit, "1.2.3.4", "/api/health") for _ in range(3)] == [200, 200, 200]


def test_idle_clients_are_forgotten():
    clock = Clock()
    limit = RateLimit(ok_app, per_minute=5, clock=clock)
    call(limit, "1.2.3.4")
    clock.now = 400
    call(limit, "5.6.7.8")
    assert list(limit.hits) == ["5.6.7.8"]
