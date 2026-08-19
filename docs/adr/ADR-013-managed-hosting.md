# ADR-013 — Managed hosting, portable by design

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The project is built by a very small team. Time spent on servers, backups, certificates and
monitoring is time not spent on the product. At the same time, being locked to one provider is a
real risk for a project that plans to run for years.

## Decision

Use **managed services**, but only ones that speak **standard protocols**, so moving is always
possible.

| Piece | Type of service | Why it is portable |
|---|---|---|
| Next.js app | Managed frontend platform | Standard Node build output |
| FastAPI app | Managed container platform | Plain Docker image |
| Worker | Same platform, second process | Same Docker image, different command |
| PostgreSQL | Managed PostgreSQL | Standard `DATABASE_URL`, plain dumps |
| Redis | Managed Redis | Standard Redis protocol |
| Storage | S3-compatible | Standard S3 API |

**Portability rules:**

1. Everything is configured by **environment variables**. No provider names inside the code.
2. The API and worker run from a **Dockerfile** that also works locally and on any server.
3. No provider-specific feature is used for anything essential. If one is used, it is written in
   this ADR as a known exception.
4. Backups must be downloadable as normal PostgreSQL dumps, and a restore is tested in Phase 36.

The exact providers are chosen in Phase 5 when the first deployment happens (open question Q15).
The document keeps `.env.example` as the real list of what must be provided.

## Alternatives considered

| Option | Why rejected |
|---|---|
| One VPS with Docker Compose | Cheapest at scale, full control, and good learning. Rejected because backups, updates, certificates, monitoring and on-call all become the developer's job, which is the wrong use of very limited time. |
| Kubernetes | Far beyond the needs of three processes. |
| Full serverless (functions per endpoint) | Cold starts hurt our p95 targets, and the graph queries want warm database connections. |
| Deep use of one cloud's own services | Fastest to build, hardest to leave, and hardest to run locally. |

## Consequences

**Good**

- Almost no server maintenance work.
- Preview environments per pull request come free with these platforms, which the Phase 5
  environment matrix already assumes.
- Free tiers cover the whole build phase.

**Cost**

- Higher price per unit of compute at large scale. Acceptable, and revisited only if real traffic
  makes it matter.
- Managed platforms have limits (request timeouts, memory caps). The crawler must respect them,
  which is another reason long work lives in the worker.
- Two providers must be kept in the same region, or server rendering pays double latency
  ([ADR-003](ADR-003-nextjs.md)).

## Revisit when

Monthly cost passes the price of a server plus the time to run it, or a platform limit blocks a
feature we need. Because everything is Docker plus environment variables, moving is a deployment
change, not a rewrite.
