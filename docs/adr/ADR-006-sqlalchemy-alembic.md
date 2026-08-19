# ADR-006 — SQLAlchemy 2.0 (async) + Alembic

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

We need typed models, real control over SQL (the graph queries are not simple), and a migration
system that produces the same database every time from an empty start.

## Decision

- **SQLAlchemy 2.0** with the async engine (`asyncpg` driver) and typed `Mapped[]` models.
- **Alembic** for migrations, one migration per change, always with a working downgrade.
- Repositories hold the queries. Services never write raw SQL directly.
- Raw SQL is allowed, but only inside a repository and only with a comment explaining why.

## Alternatives considered

| Option | Why rejected |
|---|---|
| SQLModel | Nice and short, and made by the FastAPI author. Rejected because it hides part of SQLAlchemy, and our graph and search queries need the full API. Mixing the two later is worse than starting with one. |
| Tortoise ORM / Piccolo | Smaller communities, fewer answers when something goes wrong in production. |
| Raw SQL only | Full control, but no typed models, and every developer invents their own patterns. |
| Prisma (Python client) | Its Python support is not at the level of its TypeScript version. |

## Consequences

**Good**

- Typed models catch mistakes before runtime.
- Alembic gives the "fresh database with one command, same result every time" rule from Phase 7.
- Full SQL power available when the graph queries need it.

**Cost**

- SQLAlchemy 2.0 async has a learning curve, especially around sessions and lazy loading.
- A hard rule to avoid the classic bug: **lazy loading is disabled**. Relationships must be
  loaded on purpose with `selectinload`. Otherwise an async lazy load raises errors at runtime,
  and N+1 queries appear silently.

## Revisit when

Not planned. Migrating an ORM after Phase 7 is very expensive, which is exactly why this decision
is made now rather than later.
