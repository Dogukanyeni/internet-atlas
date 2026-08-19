# ADR-008 — Background jobs with arq, behind our own interface

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

From Phase 26 onwards the system runs a lot of slow work: crawling, technology detection,
enrichment stages, AI classification, freshness checks. Phase 26 requires a queue with retry,
backoff, dead letters and scheduled jobs. The API is async, and the work is almost entirely
I/O bound.

## Decision

Use **arq** (async job queue built on Redis) for workers and scheduled jobs.

**But the application never imports arq directly.** All code calls our own thin interface:

```python
# jobs/queue.py
async def enqueue(job_name: str, *, payload: dict, run_at: datetime | None = None) -> JobId: ...
```

Job state that matters to the product (crawl jobs, pipeline stages, failures) is stored in
**PostgreSQL**, not only in Redis. Redis holds the work to be done; PostgreSQL holds the record
of what happened.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Celery | The industry standard, very mature, huge documentation, built-in scheduling with Beat. Rejected as too heavy for our needs, and its asyncio support is awkward, while our whole crawler is async. Its configuration surface is large for a solo developer. |
| RQ | Simple and popular, but synchronous, which fits our async crawler badly. |
| Dramatiq | Good design, but again sync-first and a smaller community than Celery. |
| PostgreSQL queue with `SKIP LOCKED` | No new dependency, and transactional with our data. Rejected because we already run Redis, and crawler traffic would add constant write load to the user-facing database. |
| Cloud queue (SQS and similar) | Ties us to one provider, against [ADR-013](ADR-013-managed-hosting.md). |

## Consequences

**Good**

- Async from top to bottom: an async crawler in an async worker with no bridging code.
- Small API surface — retries, timeouts and cron are a few lines of configuration.
- Only Redis is needed, which we already run.

**Cost**

- arq has a much smaller community than Celery. Fewer answers exist when something is strange.
  **This is the main risk of this ADR, and it is accepted knowingly.**
- Mitigation is the wrapper: because all code calls `jobs.enqueue()`, replacing arq with Celery
  later touches one module, not the whole codebase.
- Dead-letter handling is not built in the way Celery offers it. We implement it ourselves:
  after the final retry, the job is written to a `failed_jobs` table in PostgreSQL with its
  payload and error, so nothing is lost silently.

## Revisit when

We need features arq does not have: job chains and groups, multiple queues with priorities, or a
ready-made monitoring UI. At that point Celery becomes the likely replacement, and the wrapper
makes the change contained.
