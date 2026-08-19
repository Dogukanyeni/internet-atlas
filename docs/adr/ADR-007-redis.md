# ADR-007 — Redis for cache, rate limiting and job coordination

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

Three separate needs appear across the phases:

1. **Cache** — graph neighbourhoods, topic pages and search results are read far more often than
   they change (Phase 37).
2. **Rate limiting** — public endpoints, contribution forms, and per-domain crawl politeness
   (Phases 26 and 36).
3. **Job queue** — the worker needs somewhere to take jobs from (Phase 26).

## Decision

**One Redis instance** serves all three, with a strict key naming rule so they never collide:

| Purpose | Key prefix | Expiry |
|---|---|---|
| Cache | `cache:` | Always set, 60 s to 24 h by type |
| Rate limit | `rl:` | Equal to the window |
| Crawl politeness | `crawl:domain:` | Per-domain window |
| Queue (arq) | `arq:` | Managed by the library |
| Session lookup | `sess:` | Session lifetime |

**Rules:**

- Everything in Redis is disposable. If Redis is emptied, the product must still work — slower,
  but correct. Nothing lives only in Redis.
- Every cache key has an expiry. A key without one is a bug.
- Cache invalidation happens when an entity is published, updated or archived, by deleting keys
  by prefix for that entity.

## Alternatives considered

| Option | Why rejected |
|---|---|
| In-memory cache inside the API process | Free and fast, but wrong as soon as there is more than one process, and useless for the worker. |
| Memcached | Cache only. We also need queue and rate limiting, which would mean a second system. |
| PostgreSQL for cache and queue (`SKIP LOCKED`) | One less service, and genuinely workable. Rejected because our crawler will produce constant queue traffic, which would add load to the same database that serves user requests. |
| Separate Redis instances per purpose | Cleaner in theory. Rejected as unnecessary cost at our size; the key prefix rule is enough. |

## Consequences

**Good**

- One service covers three needs, and every managed platform offers it.
- The session store, rate limits and queue all become trivial.

**Cost**

- Redis is now a shared dependency. If it goes down, caching, limits and jobs all stop.
  Mitigation: the API must **degrade, not fail** — on a Redis error it reads from PostgreSQL and
  logs a warning. This is tested in Phase 38.
- Memory limits matter. Cache keys must always expire, or the instance fills up.

## Revisit when

Queue traffic starts to disturb cache performance. The fix at that point is a second Redis
instance for the queue, not a new technology.
