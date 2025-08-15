FROM node:22.18.0-slim AS frontend-base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

FROM frontend-base AS frontend-prod-deps
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM frontend-base AS frontend
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.13.5

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-dev

COPY --from=frontend /app/static /app/static

RUN uv run python manage.py collectstatic --noinput --clear --verbosity 2

FROM debian:bookworm-slim AS django

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  libmagickwand-dev \
  ca-certificates \
  && update-ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY --from=frontend-prod-deps /usr/local/bin/node /usr/local/bin/node
COPY --from=frontend-prod-deps /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=frontend-prod-deps /app/node_modules /app/node_modules
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
ENTRYPOINT []

FROM nginx:stable  AS nginx
RUN mkdir -p /var/run/nginx-cache/jscache
RUN echo "D /var/run/nginx-cache 0755 root root -" > /usr/lib/tmpfiles.d/nginx-cache.conf
COPY --from=builder /app/staticfiles /usr/share/nginx/html/static
COPY nginx/site.conf /etc/nginx/nginx.conf
