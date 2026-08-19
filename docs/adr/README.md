# Architecture Decision Records

Each file records one decision: why it was made, what was rejected, and when to reconsider it.

**Rules**

- An ADR is never edited to change its decision. If the decision changes, write a new ADR and set
  the old one to `Superseded by ADR-XXX`.
- Every ADR names at least one rejected alternative and the reason.
- Every ADR has a "revisit when" section. A decision with no exit condition is a belief, not a
  decision.

| ADR | Decision | Status |
|---|---|---|
| [001](ADR-001-modular-monolith.md) | Modular monolith, not microservices | Accepted |
| [002](ADR-002-python-fastapi.md) | Python 3.12 + FastAPI backend | Accepted |
| [003](ADR-003-nextjs.md) | Next.js App Router frontend | Accepted |
| [004](ADR-004-postgresql.md) | PostgreSQL as single source of truth | Accepted |
| [005](ADR-005-relations-not-graphdb.md) | Relation tables, not a graph database | Accepted |
| [006](ADR-006-sqlalchemy-alembic.md) | SQLAlchemy 2.0 async + Alembic | Accepted |
| [007](ADR-007-redis.md) | Redis for cache, rate limits and queue | Accepted |
| [008](ADR-008-background-jobs.md) | arq for background jobs, behind our interface | Accepted |
| [009](ADR-009-postgres-fts.md) | PostgreSQL full-text search first | Accepted |
| [010](ADR-010-object-storage.md) | S3-compatible object storage | Accepted |
| [011](ADR-011-openapi-typed-client.md) | OpenAPI-generated TypeScript client | Accepted |
| [012](ADR-012-session-cookies.md) | Session cookies with opaque tokens | Accepted |
| [013](ADR-013-managed-hosting.md) | Managed hosting, portable by design | Accepted |
| [014](ADR-014-monorepo.md) | One monorepo for both languages | Accepted |
