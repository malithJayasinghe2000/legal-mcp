# Hosted Rulewise MCP server (brief D23). Build: docker build -t rulewise .
FROM python:3.12-slim

RUN pip install --no-cache-dir uv==0.11.32
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project
COPY src ./src
COPY rules ./rules
RUN uv sync --locked

# Run as a normal user, not root.
RUN useradd --create-home rulewise
USER rulewise

ENV PORT=8000 RULEWISE_RATE_LIMIT=60
EXPOSE 8000
CMD ["/app/.venv/bin/rulewise", "--public"]
