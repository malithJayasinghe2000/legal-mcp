"""Per-client request limit for the hosted server (ASGI middleware).

Counts live in memory only and expire after the window: nothing is written to
disk or logs (brief D6). The client is the first address in X-Forwarded-For
(set by the hosting proxy), else the socket address.
"""

from __future__ import annotations

import json
import time
from collections import deque
from collections.abc import Callable
from typing import Any

Scope = dict[str, Any]
ASGIApp = Callable[..., Any]


class RateLimit:
    def __init__(
        self,
        app: ASGIApp,
        per_minute: int = 60,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.app = app
        self.per_minute = per_minute
        self.clock = clock
        self.hits: dict[str, deque[float]] = {}
        self.last_sweep = clock()

    def client(self, scope: Scope) -> str:
        for name, value in scope.get("headers", []):
            if name == b"x-forwarded-for":
                return value.decode("latin-1").split(",")[0].strip()
        peer = scope.get("client")
        return peer[0] if peer else "unknown"

    def allow(self, client: str) -> bool:
        now = self.clock()
        if now - self.last_sweep > 300:  # forget idle clients, so memory stays small
            self.hits = {k: v for k, v in self.hits.items() if v and now - v[-1] < 60}
            self.last_sweep = now
        window = self.hits.setdefault(client, deque())
        while window and now - window[0] >= 60:
            window.popleft()
        if len(window) >= self.per_minute:
            return False
        window.append(now)
        return True

    async def __call__(self, scope: Scope, receive: Any, send: Any) -> None:
        if scope["type"] != "http" or scope.get("path") == "/api/health":
            await self.app(scope, receive, send)
            return
        if self.allow(self.client(scope)):
            await self.app(scope, receive, send)
            return
        body = json.dumps(
            {"error": "Too many requests. The check did not run. Try again in a minute."}
        ).encode()
        await send(
            {
                "type": "http.response.start",
                "status": 429,
                "headers": [(b"content-type", b"application/json"), (b"retry-after", b"60")],
            }
        )
        await send({"type": "http.response.body", "body": body})
