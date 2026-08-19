# ADR-009 — PostgreSQL full-text search first

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

Phase 17 needs search over names, slugs, aliases and descriptions, with autocomplete and results
grouped by entity type. Our data set starts at roughly 160 websites and a few hundred topics and
technologies. The source document says to start with PostgreSQL full-text search and treat a
dedicated search engine as a separate, later stage.

## Decision

Search runs inside PostgreSQL:

- A `tsvector` column per searchable entity, kept up to date by a trigger or by the application.
- Field weights: name and slug are strongest, aliases next, description weakest.
- `pg_trgm` extension for prefix matching and simple typo tolerance in autocomplete.
- Entity type boosting is applied in the query, not hard-coded in the ranking function.

**A `SearchProvider` interface wraps all of this from day one.** Application code calls
`search.query(...)`; it never writes search SQL inline. Swapping the engine later means writing a
second implementation of one interface.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Elasticsearch / OpenSearch | Very powerful, but heavy to run, and a second copy of the data to keep in sync. Far beyond what a few hundred entities need. |
| Typesense / Meilisearch | Much lighter, excellent typo tolerance, and the likely future choice. Rejected *for now* only because it is another service to run and sync before we have any evidence we need it. |
| Vector / semantic search | Interesting for "find me something like this", but it is a Phase 30 idea, not a Phase 17 one. Users search names first. |

## Consequences

**Good**

- No new service, no synchronisation, no second source of truth.
- Search results can be filtered and joined with normal SQL, which we need for facets in
  Phase 18.
- Deleting or archiving an entity removes it from search in the same transaction.

**Cost**

- Typo tolerance is weaker than a dedicated engine. `pg_trgm` handles small mistakes;
  it will not handle badly misspelled queries.
- Ranking control is more limited.
- Search load hits the same database as everything else. Phase 37 must watch this.

## Revisit when — the written trigger

1. Users complain about typos not being found, or search analytics show many zero-result queries
   that are clearly spelling mistakes.
2. Search p95 goes above 200 ms for autocomplete after indexing work.
3. The catalog passes roughly 50,000 entities.

The `SearchProvider` interface exists so that this switch is a contained piece of work.
