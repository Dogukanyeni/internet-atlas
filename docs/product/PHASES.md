# Internet Atlas — Phase Tracker

The single place that shows where the project stands. Update the status when a phase closes.
Phase definitions and exit criteria come from `Internet_Atlas_Detayli_Proje_Dokumani.docx` v1.0.

**Status:** ✅ done · 🔵 in progress · ⬜ not started

| # | Phase | Part | Status | Deliverable |
|---|---|---|---|---|
| 0 | Product vision | I | ✅ | [00-vision.md](00-vision.md) |
| 1 | Problem and target user | I | ✅ | [01-problem-and-users.md](01-problem-and-users.md) |
| 2 | User flows | I | ✅ | [02-user-flows.md](02-user-flows.md) |
| 3 | Information architecture | I | ✅ | [03-information-architecture.md](03-information-architecture.md) |
| 4 | Architecture decisions | II | ✅ | [04-architecture.md](04-architecture.md) + [14 ADRs](../adr/) |
| 5 | Repository and standards | II | 🔵 | [05-repository.md](05-repository.md) — code done, waiting for `make setup` to run |
| 6 | Domain model and contracts | II | ⬜ | Typed interfaces, OpenAPI, error model, pagination contract |
| 7 | Database core | II | ⬜ | Migrations, ORM layer, seed script, DB integration tests |
| 8 | Authentication | III | ⬜ | Register/login, email verification, roles, auth tests |
| 9 | Website domain model | III | ⬜ | Website CRUD, validation, duplicate detection |
| 10 | Taxonomy system | III | ⬜ | Topic tree, category tree, admin editor, cycle validation |
| 11 | Relation graph | III | ⬜ | Relation tables, graph service, neighbours API |
| 12 | Admin panel base | III | ⬜ | Admin CRUD, audit log, role guards |
| 13 | Seed data | III | ⬜ | MVP catalog, import script, initial graph |
| 14 | Atlas map MVP | IV | ⬜ | Interactive graph, node/edge renderer, mobile fallback |
| 15 | Website detail | IV | ⬜ | Detail page, SEO metadata, related entities |
| 16 | Topic pages | IV | ⬜ | Topic detail, topic map, listing APIs |
| 17 | Search | IV | ⬜ | Global search, autocomplete, telemetry |
| 18 | Filtering and sorting | IV | ⬜ | Filter UI, query builder, facet API |
| 19 | Bookmarks and collections | IV | ⬜ | Bookmark button, My Library, visibility rules |
| 20 | User profile | IV | ⬜ | Profile pages, interests, privacy settings |
| 21 | Exploration paths | V | ⬜ | Path builder, viewer, progress model |
| 22 | Recommendation v1 | V | ⬜ | Rule-based recommender, reason codes |
| 23 | Community contribution | V | ⬜ | Contribution forms, proposal queue, diff viewer |
| 24 | Moderation | V | ⬜ | Moderation dashboard, state machine, abuse controls |
| 25 | Quality scoring | V | ⬜ | Score service, breakdown, versioned formulas |
| 26 | Crawler infrastructure | VI | ⬜ | Worker, crawl queue, retry/backoff, policy enforcement |
| 27 | Technology detection | VI | ⬜ | Detector framework, confidence scoring, test corpus |
| 28 | Enrichment pipeline | VI | ⬜ | Orchestrator, stage contracts, backfill tools |
| 29 | Freshness and change tracking | VI | ⬜ | Change log, history API, dead-site workflow |
| 30 | AI-assisted classification | VI | ⬜ | AI worker, prompt registry, review queue, eval set |
| 31 | Personal Atlas | VII | ⬜ | Personal graph editor, share page, visibility model |
| 32 | Browser extension | VII | ⬜ | Extension v1, auth handshake, save + suggest flows |
| 33 | Public API | VII | ⬜ | API v1, docs, API keys, quotas |
| 34 | Analytics and telemetry | VII | ⬜ | Event schema, pipeline, core dashboards |
| 35 | Observability | VII | ⬜ | Logs, metrics, tracing, runbooks, alerts |
| 36 | Security hardening | VIII | ⬜ | Threat model, scans, incident runbook, backup test |
| 37 | Performance and scalability | VIII | ⬜ | Performance budget, query optimisation, cache layer |
| 38 | Load testing and resilience | VIII | ⬜ | Load scripts, resilience scenarios, SLO dashboard |
| 39 | Beta, launch, post-launch | VIII | ⬜ | Beta release, launch checklist, rollback plan, 30/60/90 backlog |

## Locked decisions

| ID | Decision | Phase |
|---|---|---|
| V-01 | Docs, code and UI in English | 0 |
| V-02 | Real product, launch intent | 0 |
| V-03 | v1 seeds four domains: AI/ML tooling, developer tools, cloud/infra, data/databases | 0 |
| V-04 | AI enriches, never publishes by itself, never the interface | 0 |
| V-05 | PostgreSQL relation tables first; graph DB only when proven necessary | 0 |
| V-06 | Technology-focused, not a general internet index | 0 |
| P-01 | Primary persona is **The Learner** (junior/mid developer or student, new to an area) | 1 |
| P-02 | Secondary persona is **The Builder**; we serve them but do not design the MVP for them | 1 |
| P-03 | North Star Metric is **Weekly Exploring Users** (a session with 2+ relation jumps) | 1 |
| P-04 | MVP = graph + detail + topics + search. Bookmarks, paths and recommendations come after | 1 |
| P-05 | Event names are fixed in Phase 1 and never renamed after release | 1 |
| F-01 | Topic first, then map — the graph always opens around a chosen topic | 2 |
| F-02 | All exploring is open to anonymous users; an account is needed only to save or contribute | 2 |
| F-03 | We ask for an account only at the moment of saving | 2 |
| F-04 | Every screen state is deep-linkable — the URL holds focus, panel and filters | 2 |
| F-05 | The map never loads the full graph; it grows from one focus node | 2 |
| I-01 | One **Website** entity with a `kind` field — no separate Product table in v1 | 3 |
| I-02 | **Organization** is a plain text field in v1, not an entity | 3 |
| I-03 | Technology gets a light detail page in the MVP | 3 |
| I-04 | Slugs are unique per entity type and never reused; old slugs redirect forever | 3 |
| I-05 | Undirected relations are stored once, smaller id as source | 3 |
| I-06 | Public content is never hard deleted — it is archived and keeps its URL | 3 |
| A-01 | Modular monolith; API and worker are two processes from one codebase | 4 |
| A-02 | Backend: **Python 3.12 + FastAPI + Pydantic v2**, async-first | 4 |
| A-03 | Frontend: **Next.js App Router**; content pages server-rendered, map client-only | 4 |
| A-04 | **PostgreSQL 16** is the only source of truth; Redis, storage and search are derived | 4 |
| A-05 | **SQLAlchemy 2.0 async + Alembic**; lazy loading disabled | 4 |
| A-06 | Background jobs on **arq**, always behind our own `jobs.enqueue()` wrapper | 4 |
| A-07 | Types cross languages by **generated TypeScript client**; CI fails on schema drift | 4 |
| A-08 | Auth by **opaque session token in an httpOnly cookie** — never JWT in localStorage | 4 |
| A-09 | **Managed hosting**, but only standard protocols so we can move | 4 |
| A-10 | Graph limits from day one: **max depth 3, max 300 nodes** per response | 4 |
| R-01 | `make` is the only entry point; no command lives only in memory | 5 |
| R-02 | Local services run in Docker Compose, matching production versions | 5 |
| R-03 | Conventional commits, enforced by a git hook | 5 |
| R-04 | `main` is always deployable; no direct pushes | 5 |
| R-05 | Pull requests carry the Definition of Done and the vision guardrails | 5 |
| R-06 | CI is path-aware, with one always-running gate job | 5 |
| R-07 | Structured logging and request ids exist from the first commit | 5 |

## Do-not-do-early list (from the source document)

- No graph database before we measure the query load on relation tables.
- No AI recommendations before deterministic discovery is proven.
- No unlimited crawling before per-domain rate limits and a staging area exist.
- No community voting before data quality is validated.
- No browser extension before the core web experience works.
- No public API before the internal domain model is stable.
- No microservices — start with a modular monolith.
- No UI polish before search, graph, data quality and performance.
