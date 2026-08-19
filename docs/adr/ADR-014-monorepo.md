# ADR-014 — One monorepo for both languages

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4
**Set up in:** Phase 5

## Context

The project has a Python API, a Python worker, a TypeScript web app, and shared pieces such as
the generated API client and seed data. These parts change together very often: one feature
usually touches the database, the API and the UI in the same day.

## Decision

**One repository** holding both languages.

```
/
├─ apps/
│  ├─ api/          # FastAPI application (Python)
│  ├─ worker/       # arq worker entry point (shares api code)
│  └─ web/          # Next.js application (TypeScript)
├─ packages/
│  ├─ api-client/   # generated TypeScript client (ADR-011)
│  ├─ ui/           # shared React components
│  └─ config/       # shared lint, tsconfig, tooling config
├─ db/
│  ├─ migrations/   # Alembic
│  ├─ seeds/        # seed data files
│  └─ fixtures/     # test fixtures
├─ docs/
│  ├─ adr/
│  └─ product/
├─ infra/           # Dockerfiles, compose, deploy config
└─ tests/           # cross-app end-to-end tests
```

**Tooling:** `uv` for Python, `pnpm` workspaces for TypeScript, one `Makefile` (or `just` file) as
the single entry point, so a developer never needs to remember which tool belongs to which app.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Separate repositories per app | Every feature becomes several pull requests that must be merged in order. Painful for one developer, and it makes the generated client harder to keep in step. |
| Monorepo with a heavy build tool (Nx, Turborepo, Bazel) | Good caching, but extra complexity, and they are built around one language. Our split is simple enough for plain workspaces plus a Makefile. |
| Python and TypeScript in one folder with no structure | Fastest to start, and unmaintainable by Phase 10. |

## Consequences

**Good**

- One pull request contains a full feature: migration, API, generated client and UI.
- The API client generation step (ADR-011) is trivial, because both sides are in one place.
- One CI pipeline sees everything and can run the right jobs by changed path.

**Cost**

- CI must be path-aware, or every small text change runs the whole test suite. Phase 5 sets this
  up from the start.
- Two package managers exist side by side. The Makefile hides this.
- The repository grows large over time. Generated files and seed data must stay tidy.

## Revisit when

The browser extension (Phase 32) arrives. It may deserve its own repository, because it has a
different release cycle and a store review process. That is the one likely exception.
