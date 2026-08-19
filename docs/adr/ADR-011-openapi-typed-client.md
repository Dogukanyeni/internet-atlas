# ADR-011 — OpenAPI-generated TypeScript client

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The backend is Python and the frontend is TypeScript ([ADR-002](ADR-002-python-fastapi.md),
[ADR-003](ADR-003-nextjs.md)). Types are not shared automatically. The usual result is
hand-written TypeScript interfaces that slowly drift away from the real API, and the drift is
only discovered by users.

Phase 6 requires that schema drift can be **detected**, not just avoided by discipline.

## Decision

**Pydantic models are the only source of truth for API shapes.**

The pipeline:

1. FastAPI produces `openapi.json` from the Pydantic models.
2. A generator produces a typed TypeScript client into `packages/api-client`.
3. The generated client is **committed to the repository**, so builds are repeatable and the
   frontend does not need a running backend to compile.
4. **CI regenerates the client and fails the build if the result differs from what is committed.**

**Rules:**

- No hand-written TypeScript interface may describe an API response. Ever.
- The frontend imports types only from `packages/api-client`.
- An API change that breaks the frontend now fails in CI, at pull request time.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Hand-written types on the frontend | Fast on the first day, wrong within a month, and the errors reach users. |
| Contract tests only | Catches drift, but later and with more work than simply generating the client. |
| GraphQL with generated types | Solves this problem well, but adds a whole query layer we do not need yet (see `04-architecture.md` §9). |
| tRPC | Excellent, but it requires TypeScript on both sides, which we rejected in ADR-002. |

## Consequences

**Good**

- Renaming a field in Python immediately shows every broken place in the frontend.
- The API documentation is generated from the same source, so it cannot go stale.
- New frontend work gets autocomplete for every endpoint and field.

**Cost**

- One more CI step, and one more thing to run after changing a model. Phase 5 must provide a
  single command like `make api-client` so it is never a manual chore.
- Generated code is noisy in pull requests. It lives in its own package and is marked as
  generated so reviewers can skip it.
- The generator must be pinned to an exact version. A generator upgrade changes many files at
  once and should be its own pull request.

## Revisit when

The API becomes public and has many external clients (Phase 33). At that point the public API
gets its own versioned schema, separate from this internal client.
