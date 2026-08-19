# Phase 0 — Product Vision

**Status:** Locked · **Version:** 1.0 · **Date:** 2026-08-19
**Source:** `Internet_Atlas_Detayli_Proje_Dokumani.docx` v1.0 (2026-08-18)

This document is the fixed point of the project. Every later phase is measured against it.
It can only be changed with a version bump and a note in the changelog at the bottom —
never quietly, and never to justify a feature that was already built.

---

## 1. One-sentence definition

> **Internet Atlas is a discovery platform that shows software, technology and the digital
> ecosystem around them as an explorable graph of websites, technologies, topics and the
> relationships between them.**

If a feature cannot be traced back to this sentence, it is out of scope.

---

## 2. Product thesis

Search engines are built for **ending**: you type a query, you get an answer, you leave.
That works when you know what you are looking for. It fails when you do not — when the real
question is *"what exists in this area, and where do I go next?"*

Internet Atlas is built for **continuing**. The user does not consume a result; they move
through a subject. Every object in the Atlas is a place you can stand, and every place has
visible exits.

| | Search engine | Internet Atlas |
|---|---|---|
| Unit of value | The answer | The route |
| Success signal | User leaves quickly | User goes one step further |
| Structure | Flat ranked list | Typed graph you can navigate |
| Ends when | The query is answered | The user decides to stop |
| Fails when | User cannot name what they want | User has one precise question |

We accept being the *worse* tool for a precise question. That is a search engine's job.

---

## 3. The four core behaviours

These must exist for the product to be itself. Everything else is optional.

1. **Navigate, do not query.** The main interaction is moving between connected objects, not
   typing search terms again and again. Search only drops you into the graph.
2. **Every object has context.** A website is never shown alone. It comes with its categories,
   technologies, alternatives, integrations and competitors. A page with no outgoing relations
   is a bug, not an empty record.
3. **The user builds their own route.** Two users starting at the same node should be able to
   leave in completely different directions, and keep what they found.
4. **Trust is visible.** Where a fact came from, when it was last checked, and how sure we are,
   are shown in the UI — not hidden in the database.

### Product vocabulary

One phrase, used everywhere: in UI text, analytics names and internal discussion.

**Discover → Understand → Explore**

- **Discover** — the user finds something they did not know existed (map, search, topic page).
- **Understand** — the user gets enough context to judge it (website detail, technologies).
- **Explore** — the user moves to the next thing through a relation (graph, alternatives, paths).

A feature that serves none of these three does not belong in the product.

---

## 4. Scope

### 4.1 In scope

| Layer | Included |
|---|---|
| Entities | Websites, products, technologies, topics, categories, organizations, relations, paths, collections |
| Capability | Graph exploration, website detail, topic pages, search, filtering, saving, curated routes |
| Data work | Editorial curation, community proposals with moderation, crawling, technology detection, AI-assisted classification under human review |
| Domains (v1) | See 4.3 |

### 4.2 Out of scope — permanently

These are not "later". They are things Internet Atlas is not. Requests to add them are answered
by pointing at this section.

- A general web index or a directory of all websites.
- A news portal or content feed.
- A social network — following, timelines and a social graph are not the product.
- Trading, portfolio or investment-advice features.
- A hosting platform for content on any subject.
- An AI chatbot. AI works inside the product, never as its interface.

### 4.3 v1 content scope — deliberately narrow

The source document lists ten possible domains. Seeding all ten with 20–50 sites each gives a
graph that is *wide and thin*: every direction looks almost empty, which feels broken rather
than young. Density is the feature. **v1 seeds four neighbouring domains that really connect:**

1. **AI & ML tooling** — model providers, frameworks, agent tools, vector stores, eval tools.
2. **Developer tools** — languages, frameworks, editors, CI/CD, testing, package ecosystems.
3. **Cloud & infrastructure** — hosting, serverless, containers, CDN, observability, DevOps.
4. **Data & databases** — relational, NoSQL, warehouses, pipelines, BI, streaming.

These four were chosen because the relations between them are facts, not opinions:
`built_with`, `integrates_with`, `alternative_to` and `part_of` edges appear naturally and often
across their borders (a hosting platform runs a runtime, an agent framework integrates with a
vector store, one warehouse competes with another).

Domains kept for v2+: SaaS, open source (as its own axis), design tools, fintech, security,
productivity. **The architecture must not assume four domains** — this is a seeding decision,
not a schema decision.

---

## 5. Definition of success

Phase 0 defines success as behaviour. The single North Star Metric and its metric tree are
**Phase 1 deliverables** and are deliberately not fixed here.

### 5.1 Behavioural targets

| # | Statement | Target | Measured from |
|---|---|---|---|
| S1 | A new visitor reaches something useful fast | First real node view within **3 minutes** | Phase 34 telemetry |
| S2 | Exploring actually happens | Median session has **≥ 2 relation jumps** | `relation_click` events |
| S3 | The graph is not a dead end | **≥ 60%** of website-detail sessions continue to another node | funnel |
| S4 | Users come back to what they saved | **≥ 25%** of registered users return within 7 days | retention cohort |
| S5 | The Atlas is never empty | **≥ 5** complete exploration routes work at seed completion | Phase 13 exit check |

### 5.2 Data-quality targets

| # | Statement | Target |
|---|---|---|
| D1 | Nothing is without context | **100%** of published websites have ≥ 1 category and ≥ 2 relations |
| D2 | Every claim has a source | **100%** of published relations carry `provenance` and `confidence` |
| D3 | Freshness is honest | Every published website shows a `last_verified` date |
| D4 | Seed density is real | ~**160** websites and ~**500** relations across the four v1 domains |

### 5.3 System targets

The platform starts with hundreds of curated objects and must grow to tens of thousands through
the Part VI data engine **without a schema rewrite**. If a Phase 6/7 modelling decision would
have to be undone at 10,000 websites, it is the wrong decision.

---

## 6. Vision guardrails

Every phase exit answers these seven questions. A "no" blocks the phase.

1. Does this make the graph **denser or more trustworthy**, or only bigger?
2. Can the user still see **where to go next** from every screen we shipped?
3. Is any AI output reaching the public graph **without human review**? (must be no)
4. Does every new fact carry **provenance, confidence and a verified date**?
5. Did we build a **list** where a **graph** was the point?
6. Would a first-time visitor understand the product within **one screen**?
7. Are we polishing the UI before search, graph, data quality and performance are solid?

---

## 7. Decisions locked in Phase 0

| ID | Decision | Reason |
|---|---|---|
| V-01 | Documentation, code and product UI are in **English** | The audience is global, the vocabulary is already English, and topic SEO is better |
| V-02 | Built as a **real product with launch intent** | Phases 26–39 are only reachable with CI, tests, migrations and observability from Part II |
| V-03 | v1 seeds **four neighbouring domains**, not ten | Graph density is the differentiator; a thin graph looks broken |
| V-04 | AI is an **enrichment layer**, never the interface, and never publishes by itself | Accuracy and trust are the moat; invented relations destroy it |
| V-05 | **Relation tables in PostgreSQL** first; graph DB only when queries prove the need | Avoids paying a big cost before there is load to justify it |
| V-06 | Technology-focused Atlas, **not** a general internet index | Keeps quality possible for a small team |

---

## 8. Anti-vision — the failures we name in advance

- **It became a directory.** Rows of cards, alphabetical, no edges. The graph was decoration.
- **It became a worse search engine.** People type, read one result, leave.
- **It became an AI wrapper.** A chat box on scraped data, like everything else.
- **It became stale.** Crawled once in 2026, never checked again, half the links dead.
- **It became a maze.** A beautiful graph with no entry point and no way out.

Each one is a realistic result of building the right features in the wrong order. The phase
order exists to prevent them.

---

## 9. Open questions — deferred, with owners

| # | Question | Answered in |
|---|---|---|
| Q1 | Persona definitions and use-case matrix | Phase 1 ✅ |
| Q2 | North Star Metric and supporting metrics | Phase 1 ✅ |
| Q3 | First-visit entry point: map, topic list, or search | Phase 2 ✅ |
| Q4 | Is `Product` a separate entity from `Website` in v1? | Phase 3 ✅ (no) |
| Q5 | How deep can anonymous users explore before signup? | Phase 2 ✅ |
| Q6 | Monetisation position (affects Phase 33 API quotas) | Phase 33, not earlier |
| Q7 | Brand name, domain and visual identity | Before Phase 14 |

---

## 10. Phase 0 exit criteria

- [x] One-sentence definition exists and is clear
- [x] Core behaviours defined without depending on any UI
- [x] In-scope and out-of-scope written, including permanent non-goals
- [x] v1 content scope narrowed, with a reason
- [x] Success defined as behaviour, with measurable targets
- [x] Guardrails written so later phases can be tested against them
- [x] Open questions assigned to specific later phases

**Phase 0 is closed. Next: Phase 1 — Problem and target user.**

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-19 | First vision lock from the source document; decisions V-01…V-06 recorded |
