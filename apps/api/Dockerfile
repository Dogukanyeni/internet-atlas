# One image runs both the API and the worker (ADR-001).
# Only the start command differs, which is set by the platform.

FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# uv installs dependencies much faster than pip and reads pyproject.toml directly.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Dependencies first, so Docker can cache this layer between code changes.
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project || uv sync --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# The app must never run as root (Phase 36).
RUN useradd --create-home --uid 1001 atlas && chown -R atlas:atlas /app
USER atlas

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health/live').status==200 else 1)"

# API. The worker overrides this with:
#   arq atlas.jobs.worker.WorkerSettings
CMD ["uvicorn", "atlas.main:app", "--host", "0.0.0.0", "--port", "8000"]
