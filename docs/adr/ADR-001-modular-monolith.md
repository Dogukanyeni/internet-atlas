# ADR-001 — Modular monolith, not microservices

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The project has 40 phases and many domains: catalog, taxonomy, graph, search, crawling, AI,
moderation. It is built by a very small team. Splitting domains into separate services early is a
common instinct, and a common way to fail.

## Decision

We build **one application** with strong internal module boundaries. It is deployed as
**two processes from the same codebase**: the API and the background worker.

Module boundaries are folders with import rules (see `04-architecture.md` §4). A module talks to
another module only through its service layer, never by reaching into its internals.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Microservices per domain | Network calls, separate deploys, distributed transactions and tracing — all cost paid before there is any load to justify it. The source document explicitly warns against this. |
| One process for everything, including jobs | A slow crawl would block user requests. We need at least the worker separated. |
| Serverless functions per endpoint | Cold starts hurt our p95 targets, and the graph code needs warm database connections. |

## Consequences

**Good**

- One codebase, one test suite, one migration history.
- A change that crosses catalog and graph is one pull request, not three.
- Moving a module out later is possible, because the boundary already exists.

**Cost**

- Boundaries are only as strong as our discipline. They must be checked in review, and later by
  an automatic import rule.
- The whole app is deployed together, so one bad change can affect everything. CI must be strict.

## Revisit when

One module needs to scale independently in a way that hurts the rest — most likely `ingest`
during heavy crawling. Even then, moving the worker to its own scaling group comes before
splitting the code.
