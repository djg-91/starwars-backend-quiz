FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_HTTP_TIMEOUT=60

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY shared ./shared

# --- API ---
FROM base AS api

COPY api ./api

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- CLI ---
FROM base AS cli

COPY cli ./cli

ENTRYPOINT ["uv", "run", "python", "-m", "cli.main"]
