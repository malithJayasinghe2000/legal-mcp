# Hosted Rulewise MCP server (brief D23). Build for Azure (Intel/AMD servers):
#   docker buildx build --platform linux/amd64 -t rulewise .
# uv runs only in the first stage, on the build machine's own chip: under emulation
# (Apple chip building for amd64) uv crashes, pip does not.

FROM --platform=$BUILDPLATFORM python:3.12-slim AS lock
RUN pip install --no-cache-dir uv==0.11.32
WORKDIR /lock
COPY pyproject.toml uv.lock ./
# The exact versions from uv.lock, without dev tools or the project itself.
RUN uv export --locked --no-dev --no-emit-project --no-hashes -o requirements.txt

FROM python:3.12-slim
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY --from=lock /lock/requirements.txt .
RUN pip install -r requirements.txt
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY rules ./rules
RUN pip install --no-deps . && rm -rf /app/src

# Run as a normal user, not root.
RUN useradd --create-home rulewise
USER rulewise

ENV PORT=8000 RULEWISE_RATE_LIMIT=60
EXPOSE 8000
CMD ["rulewise", "--public"]
