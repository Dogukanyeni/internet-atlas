# ADR-002 — Python 3.12 + FastAPI for the backend

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The backend is domain-heavy: relation logic, scoring, taxonomy rules, plus a large data engine in
Part VI (crawler, technology detection, enrichment, AI classification). The developer is
strongest in Python.

## Decision

The API is **Python 3.12 with FastAPI and Pydantic v2**, written async-first.
Package management with **uv**. Formatting and linting with **ruff**. Type checking with **mypy**
in strict mode for the `modules/` folder.

## Alternatives considered

| Option | Why rejected |
|---|---|
| TypeScript backend (NestJS / Fastify) | One language across the stack and free type sharing, which is a real advantage. Rejected because the developer is stronger in Python, and Phases 26–30 (crawling, parsing, detection, AI) are much better served by the Python ecosystem. |
| Django + DRF | Batteries included and a free admin panel, but heavier and more opinionated. Its ORM is sync-first, which fights our async crawler. Our admin panel needs custom graph editing anyway. |
| Go | Excellent for the crawler, weaker for fast product iteration and AI tooling. |

## Consequences

**Good**

- Pydantic v2 gives validation and OpenAPI generation from the same models.
- Async fits an I/O-heavy product: many small database and HTTP calls.
- The crawler, parsers, detectors and AI clients all live in their natural ecosystem.

**Cost**

- Types are not shared with the frontend automatically. This is solved by
  [ADR-011](ADR-011-openapi-typed-client.md) — generated client, checked in CI.
- Two toolchains in one repository (uv and pnpm). Phase 5 must make both start with one command.
- Async Python needs care: one blocking call inside an async function stalls the event loop.
  Rule: any CPU-heavy or blocking work goes to the worker or `run_in_threadpool`.

## Revisit when

Never for v1. If the API layer ever becomes a thin pass-through and all logic moves to workers,
the language choice can be re-examined — but that is not a foreseeable state.
