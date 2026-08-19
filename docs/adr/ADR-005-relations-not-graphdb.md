# ADR-005 — Relation tables in PostgreSQL, not a graph database

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4
**Comes from:** vision decision V-05

## Context

The graph is the product. It is tempting to reach for a graph database on day one. But our real
query shapes are narrow, and the source document explicitly lists "moving to a graph database too
early" as a mistake to avoid.

Our actual queries are:

1. Neighbours of one node, filtered by relation type — **depth 1**
2. Neighbourhood for the map — **depth 2, sometimes 3**, always with a node limit
3. "Alternatives to X", "what is X built with" — **depth 1** with a type filter
4. Path building — a hand-made ordered list, not a graph search

None of these need graph algorithms. There is no shortest path, no community detection, no
page-rank in the MVP.

## Decision

Store relations in a **PostgreSQL table**:

```
relations(id, source_id, source_type, target_id, target_type,
          type, weight, confidence, provenance, status, note, ...)
```

- Indexes on `(source_id, type)` and `(target_id, type)`.
- A unique index that prevents duplicate edges, using the smaller-id rule from decision I-05.
- Depth 1 is a simple indexed select.
- Depth 2–3 uses `WITH RECURSIVE` with a hard node limit.
- Results are cached in Redis.

**Hard limits from the first day:** maximum depth 3, maximum 300 nodes per response.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Neo4j or a dedicated graph database | A second source of truth, a second query language, a second thing to back up and sync. Real benefit only appears with deep traversal we do not have. |
| PostgreSQL with the Apache AGE extension | Graph queries inside Postgres, which is attractive. Rejected because managed providers rarely offer the extension, and it would tie us to a specific host. |
| Keeping the whole graph in memory | Fast, and fine at 160 websites. Fails as soon as the data engine grows the graph, and it makes every process stateful. |

## Consequences

**Good**

- One database, one backup, one set of transactions.
- Relations get normal constraints: no duplicates, no self relations, valid type pairs.
- Any developer who knows SQL can work on the graph.

**Cost**

- Recursive queries need care and hard limits, or they become the slowest thing in the system.
- Layout and ranking are computed in application code, not by the database.

## Revisit when — the written trigger

We re-open this ADR only if **one** of these becomes true:

1. A normal exploration query needs depth 4 or more.
2. The recursive query p95 goes above 300 ms with production data, after indexes and caching.
3. A real feature needs a graph algorithm (shortest path between two tools, clustering).

Until one of those happens, the answer to "should we use a graph database" is **no**, and this
document is the answer.
