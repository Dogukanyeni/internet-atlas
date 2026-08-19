# Phase 5 — Repository and Development Standards

**Status:** Locked · **Version:** 1.0 · **Date:** 2026-08-19
**Depends on:** [04-architecture.md](04-architecture.md) and the ADR set

This is the first phase that produces code. It produces almost no product code on
purpose. What it produces is the floor everything else stands on: one command to start,
one command to check, and rules that a tired developer still follows.

---

## 1. What exists now

```
C:\Internet_Atlas\
├─ apps/
│  ├─ api/          FastAPI app: config, logging, errors, db, redis, health, jobs
│  ├─ worker/       thin entry point, shares the api code
│  └─ web/          Next.js app with a placeholder page
├─ packages/
│  ├─ api-client/   generated schema lives here (ADR-011)
│  ├─ ui/           empty until Phase 14
│  └─ config/       shared TypeScript tooling
├─ db/              migrations, seeds, fixtures (filled in Phase 7 and 13)
├─ docs/
│  ├─ product/      one document per phase
│  └─ adr/          14 architecture decisions
├─ infra/           deployment configuration
├─ .github/         CI pipeline and pull request template
├─ Makefile         the only entry point a developer needs
├─ docker-compose.yml
└─ .env.example
```

## 2. The one-command rule

A developer should never need to remember which tool belongs to which app. Everything
goes through `make`:

| Command | What it does |
|---|---|
| `make setup` | Install everything, create `.env`, install git hooks |
| `make up` / `make down` | Start / stop PostgreSQL, Redis, MinIO |
| `make api` / `make web` / `make worker` | Run each application |
| `make check` | Lint, type check and test — exactly what CI runs |
| `make format` | Fix style automatically |
| `make openapi` | Regenerate the API schema |
| `make reset` | Delete local data and start fresh |

This is the Phase 5 exit rule in practice: a new machine goes from nothing to a running
project with `make setup`, `make up`, `make api`.

## 3. What was built in the API, and why so little

Only the parts that are painful to add later:

| Piece | Why it is here in Phase 5 |
|---|---|
| `core/config.py` | Settings from environment variables, validated at boot. A missing variable stops the app immediately instead of failing confusingly hours later. |
| `core/logging.py` | Structured logging with a request id from the first line of code. Adding this in Phase 35 would mean rewriting every log call. |
| `core/errors.py` | One error shape for the whole API. Internal details never reach the client. |
| `core/db.py` | Async engine and session, with lazy loading disabled (ADR-006). |
| `core/redis.py` | One client, with the key prefixes fixed in one place (ADR-007). |
| `modules/health/` | Live, ready and info endpoints. Hosting platforms need them, and readiness proves the database and Redis really connect. |
| `jobs/queue.py` | The `enqueue()` wrapper, so no module ever imports arq directly (ADR-008). |
| `scripts/export_openapi.py` | Makes schema drift detectable in CI (ADR-011). |

Everything else waits for its phase. There are no models, no migrations and no product
endpoints yet — that is Phase 7 onwards.

### One design detail worth naming

`/health/ready` returns **200 with `degraded`** when Redis is down, but **503** when the
database is down. This is ADR-007 turned into behaviour: without Redis we are slower,
not broken, so the platform should not take the whole service out of rotation.

## 4. Standards that are now enforced, not just written

| Rule | Enforced by |
|---|---|
| Python style and lint | `ruff` in pre-commit and CI |
| Python types | `mypy --strict` on `src/` in CI |
| No `print()` in the API | ruff rule `T20` |
| No `any` in TypeScript | eslint rule, error level |
| Conventional commit messages | `conventional-pre-commit` git hook |
| No `.env` committed | `.gitignore` plus a pre-commit hook that blocks it |
| No private keys committed | `detect-private-key` hook |
| No huge files committed | `check-added-large-files`, 1 MB limit |
| API schema matches the code | CI job fails on drift (ADR-011) |
| Line endings stay LF | `.editorconfig` and `mixed-line-ending` hook |

The point of putting these in hooks and CI is that they keep working on the day nobody
feels like being careful.

## 5. CI pipeline

Three jobs plus a gate:

1. **changes** — works out whether the API, the web app, or both were touched.
2. **api** — format check, lint, type check, tests with a real PostgreSQL and Redis,
   then the OpenAPI drift check.
3. **web** — lint, type check, production build.
4. **ci** — always runs, and is the single required check for branch protection.

The fourth job exists to avoid a common trap: if the only required checks are jobs that
can be skipped, a documentation-only pull request waits forever for a check that will
never run.

## 6. Secrets

- Everything is an environment variable. `.env.example` is the full list.
- `.env` is git-ignored, and a hook blocks it even if someone forces it.
- `ATLAS_SECRET_KEY` must be at least 32 characters, checked at startup.
- The crawler and AI calls are **off by default** in every environment except
  production, so a laptop cannot start a real crawl and an AI bill cannot appear by
  accident.

## 7. Decisions locked in Phase 5

| ID | Decision |
|---|---|
| R-01 | `make` is the only entry point; no command lives only in someone's memory |
| R-02 | Local services run in Docker Compose and match production versions |
| R-03 | Conventional commits, enforced by a git hook |
| R-04 | `main` is always deployable; no direct pushes |
| R-05 | Pull requests carry the Definition of Done checklist and the vision guardrails |
| R-06 | CI is path-aware, with one always-running gate job |
| R-07 | Structured logging and request ids exist from the first commit |

## 8. Phase 5 exit criteria

- [x] Monorepo structure created, matching ADR-014
- [x] One-command local setup (`make setup`, `make up`, `make api`)
- [x] Lint, format, type check and tests run locally and in CI
- [x] Commit hooks installed, including conventional commits
- [x] Environment variable schema written and validated at boot
- [x] README, CONTRIBUTING, LOCAL_SETUP and ADR folder in place
- [x] Pull request template with Definition of Done
- [x] Git repository initialised with a clean first commit
- [ ] **Open:** developer runs `make setup` successfully on this machine (needs Docker,
      uv and pnpm installed — see [LOCAL_SETUP.md](../LOCAL_SETUP.md))

**Phase 5 is closed once the setup runs on your machine. Next: Phase 6 — Domain model and data contracts.**

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-19 | Repository created: monorepo, Docker Compose, CI, hooks, health endpoints, job wrapper. |
