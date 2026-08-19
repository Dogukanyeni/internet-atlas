# Internet Atlas

A discovery platform that shows software, technology and the digital ecosystem around
them as an explorable graph of websites, technologies, topics and the relationships
between them.

Search engines are built for **ending** a question. Internet Atlas is built for
**continuing** one.

> **Status:** Phase 5 of 39. The repository and standards are ready.
> The product experience starts at Phase 14.
> Current progress: [`docs/product/PHASES.md`](docs/product/PHASES.md)

---

## Quick start

**You need:** [Docker Desktop](https://www.docker.com/products/docker-desktop/),
Python 3.12, Node 22+, [uv](https://docs.astral.sh/uv/), and pnpm.

```bash
make setup     # install dependencies, create .env, install git hooks
make up        # start PostgreSQL, Redis and MinIO
make api       # http://localhost:8000  (docs at /docs)
make web       # http://localhost:3000
```

Full instructions, including how to install the missing tools:
[`docs/LOCAL_SETUP.md`](docs/LOCAL_SETUP.md)

Run `make` with no arguments to see every command.

## Repository layout

```
apps/
  api/        FastAPI application — the modular monolith
  worker/     background worker entry point (shares the api code)
  web/        Next.js application
packages/
  api-client/ TypeScript client generated from the API schema
  ui/         shared React components
  config/     shared tooling configuration
db/
  migrations/ Alembic migrations
  seeds/      seed data
  fixtures/   test fixtures
docs/
  product/    one document per phase
  adr/        architecture decision records
infra/        Dockerfiles and deployment configuration
```

## The stack

| Area | Choice | Why |
|---|---|---|
| Backend | Python 3.12 + FastAPI | [ADR-002](docs/adr/ADR-002-python-fastapi.md) |
| Frontend | Next.js App Router | [ADR-003](docs/adr/ADR-003-nextjs.md) |
| Database | PostgreSQL 16 | [ADR-004](docs/adr/ADR-004-postgresql.md) |
| Graph | Relation tables, no graph database | [ADR-005](docs/adr/ADR-005-relations-not-graphdb.md) |
| Jobs | arq on Redis | [ADR-008](docs/adr/ADR-008-background-jobs.md) |
| Search | PostgreSQL full-text first | [ADR-009](docs/adr/ADR-009-postgres-fts.md) |

All 14 decisions: [`docs/adr/`](docs/adr/README.md)

## Where to start reading

1. [Product vision](docs/product/00-vision.md) — what this is, and what it will never be
2. [Problem and users](docs/product/01-problem-and-users.md) — who it is for, and the one metric
3. [User flows](docs/product/02-user-flows.md) — screens and states
4. [Information architecture](docs/product/03-information-architecture.md) — entities and relations
5. [Architecture](docs/product/04-architecture.md) — the technical system

## Contributing

[`CONTRIBUTING.md`](CONTRIBUTING.md) — branches, commits, standards and the definition of done.
