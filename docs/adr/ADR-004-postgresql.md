# ADR-004 — PostgreSQL as the single source of truth

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The data is relational: websites belong to categories, topics form trees, relations connect
nodes, users own collections. We also need transactions (publishing a website and its relations
must succeed or fail together), full-text search at the start, and JSON storage for crawler
output.

## Decision

**PostgreSQL 16** holds all durable data. Everything else — Redis, object storage, later a search
engine — is a **derived copy** and can be rebuilt from PostgreSQL.

Features we will use on purpose:

- `jsonb` for crawler results and AI output that has no fixed shape yet
- `tsvector` for full-text search (see [ADR-009](ADR-009-postgres-fts.md))
- `WITH RECURSIVE` for graph traversal and topic trees
- Partial and composite indexes for the relation table
- Check constraints for status values and score ranges

## Alternatives considered

| Option | Why rejected |
|---|---|
| MongoDB | Our data is deeply relational and needs constraints. Duplicate prevention and referential integrity are core product requirements, not extras. |
| MySQL | Workable, but weaker `jsonb`, weaker full-text search, and no equally good recursive query story. |
| SQLite for early phases | Fine locally, but different behaviour from production. The document requires reproducible migrations, so we use the real database everywhere. |

## Consequences

**Good**

- One place to back up, one place to restore, one place where truth lives.
- Constraints stop bad data at the database level, not only in application code.
- Cheap and available from every managed provider.

**Cost**

- Some queries (deep graph traversal) are harder than in a graph database. Accepted knowingly in
  [ADR-005](ADR-005-relations-not-graphdb.md).
- We must be careful with indexes: the document warns against adding an index to every column.
  Indexes are added from real queries, and each one is justified in the migration.

## Revisit when

Never for the source of truth. Only the *derived* systems (search, graph) may move elsewhere.
