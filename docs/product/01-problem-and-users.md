# Phase 1 — Problem and Target User (PRD v1)

**Status:** Locked · **Version:** 1.0 · **Date:** 2026-08-19
**Depends on:** [00-vision.md](00-vision.md)

This document answers three questions: **who has the problem**, **what we build for them**,
and **what we do not build**. If a future feature request does not fit this document,
the answer is no.

---

## 1. The problem

A person wants to learn a new area of technology. For example: "I want to build an AI agent",
or "I need to move my app to the cloud".

Today they have three bad options:

| Option | Why it fails |
|---|---|
| Search engine | You must already know the name of the thing you are looking for. If you do not know that "vector database" exists, you cannot search for it. |
| "Top 10 tools" blog posts | Written once, never updated. Often paid. No connection between the tools. |
| Asking people | Slow. The answer depends on who you ask, and you get opinions, not a map. |

All three give you **items**. None of them give you a **map**.

The missing thing is context: what exists in this area, how the pieces connect,
what is an alternative to what, and what is built on top of what.

**Internet Atlas solves this by showing the connections, not just the items.**

---

## 2. Who we build for

### 2.1 Primary persona — "The Learner"

**Short description:** a junior or mid-level developer, or a student, who is entering a new
technical area and does not yet know what exists in it.

| Attribute | Detail |
|---|---|
| Experience | 0–4 years in software |
| Situation | Learning a new area for a job, a course, a side project, or curiosity |
| Knows | The general goal ("I want to build X") |
| Does not know | The names of the tools, who competes with who, what is standard, what is dead |
| Feeling | A little lost. Afraid of picking the wrong tool and wasting weeks. |
| Where they are now | YouTube, blog posts, Reddit, Discord, asking friends |

**Why this persona is first:** they get the most value from a map, and they are the easiest
group to serve well with a small database. A learner does not need 10,000 websites.
They need 40 correct ones with clear connections. This matches our v1 seed plan exactly.

**Their 7 key scenarios:**

| # | Scenario | What they do in Atlas | Phase that enables it |
|---|---|---|---|
| L1 | "I am new to this area. What exists here?" | Open a topic page, see the main tools and how they group | 16 |
| L2 | "Everyone talks about this tool. What is it, really?" | Open the website detail page, read the short summary and its categories | 15 |
| L3 | "Is there a cheaper or simpler option?" | Follow `alternative_to` relations from the tool | 11, 15 |
| L4 | "What is this popular site built with?" | Look at the technologies on the website detail page | 27 |
| L5 | "These two names keep appearing together. Why?" | See the relation between them and its type | 11, 14 |
| L6 | "I found something good. I do not want to lose it." | Save it to a collection | 19 |
| L7 | "Where do I start? Just tell me the order." | Follow a curated exploration path | 21 |

### 2.2 Secondary persona — "The Builder"

**Short description:** a working developer, tech lead or founder who must choose a tool for a
real project soon.

| Attribute | Detail |
|---|---|
| Experience | 4+ years |
| Situation | Making a real decision with real cost |
| Knows | The problem very well, and 1–2 tool names |
| Does not know | The full list of options, and what breaks later |
| Needs | Correct data, alternatives, integrations, and proof of freshness |
| Risk for us | This user notices wrong data immediately and does not come back |

**Their key scenarios:**

| # | Scenario | What they do in Atlas | Phase |
|---|---|---|---|
| B1 | "Show me every real alternative to this tool" | Filter by category, follow `alternative_to` edges | 11, 18 |
| B2 | "Does this work with our existing stack?" | Follow `integrates_with` edges | 11, 15 |
| B3 | "Is this project still alive?" | Check the freshness badge and last verified date | 29 |
| B4 | "What do companies like ours actually use?" | Explore by technology and category | 27 |
| B5 | "I know this area. Your data is wrong here." | Send a correction as a contribution | 23 |

We serve The Builder, but we do **not** change the product for them in the MVP.
They arrive naturally once the data is good.

### 2.3 Anti-persona — who we do not serve

Writing this down protects the roadmap.

- **The person with one precise question.** ("What is the syntax for X?") A search engine is
  better for them, and we should not try to win this.
- **The general web surfer** looking for news, shopping or entertainment.
- **The SEO spammer** who wants a backlink. Our moderation exists partly to stop them.
- **The investor** looking for market data or financial advice. This is a permanent non-goal.

---

## 3. The persona matrix

The four questions the source document asks for each persona.

| | The Learner (primary) | The Builder (secondary) |
|---|---|---|
| **Why do they come?** | They are lost in a new area and want to see the whole picture | They must choose a tool and want to see all real options |
| **What do they do?** | Explore a topic, jump between connected tools, save what looks useful | Compare alternatives, check integrations, check if a project is alive |
| **What value do they get?** | A mental map of the area, and confidence about where to start | A short, correct list of options with the reasons behind it |
| **Why do they come back?** | Their saved collection is here, and the next learning topic is one click away | The data stays fresh, and it is faster than searching again |

---

## 4. Non-goals

Internet Atlas is **not**:

1. **A search engine.** We do not index the whole web and we do not compete on precise answers.
2. **A finance or investment tool.** No market data, no advice, no company valuations.
3. **A social network.** No feed, no following people, no timeline, no likes as the main mechanic.
4. **A general wiki.** We do not host long articles on every subject. We describe and connect.
5. **A news site.** We do not publish daily content.
6. **An AI chatbot.** AI works inside the system. It is never the front door.
7. **A paid ranking or ad platform.** Nobody can buy a position in the graph. This is a trust rule.

---

## 5. Product language

We use the same three words everywhere: in the UI, in the code, in analytics, and in meetings.

**Discover → Understand → Explore**

| Beat | Meaning for the user | Main screens |
|---|---|---|
| Discover | "I did not know this existed" | Map, search, topic page |
| Understand | "Now I know what it is and if it fits me" | Website detail |
| Explore | "Now I know where to go next" | Relations, alternatives, paths |

A feature that does not serve one of these three is out of scope.

---

## 6. North Star Metric

### 6.1 The metric

> **Weekly Exploring Users (WEU)** — the number of unique users in a 7-day window who complete
> at least one session with **2 or more relation jumps**.

**Exact definition, so it cannot drift:**

- **Unique user** = a logged-in user id, or an anonymous id if not logged in. Both count.
- **Session** = activity with no gap longer than 30 minutes.
- **Relation jump** = a `relation_click` event, meaning the user moved from one node to a
  connected node on purpose. Back button and page reload do not count.
- **Window** = rolling 7 days.

### 6.2 Why this metric

- It measures the **one behaviour that defines the product**. If people only search and leave,
  we have built a worse search engine, and this number stays flat.
- It is **hard to fake**. Traffic spikes do not move it. Only real exploring does.
- It works **from Phase 14**, so we get feedback early.
- It is honest about failure. A pretty map that nobody explores scores zero.

### 6.3 The metric tree

WEU goes up only if these four inputs go up. Each one has an owner phase.

| Level | Metric | Target | Phase |
|---|---|---|---|
| Input 1 — Arrival | Visitors who reach their first node view | ≥ 70% of sessions | 14–17 |
| Input 2 — Exploration | Relation clicks per node view | ≥ 0.6 | 11, 14, 15 |
| Input 3 — Graph density | Average published relations per website | ≥ 4 | 13, 23, 27 |
| Input 4 — Return | Users who return within 7 days | ≥ 25% | 19, 20, 22 |

**Guardrail metrics** (these must not get worse while we push WEU up):

| Guardrail | Limit |
|---|---|
| Broken or dead links shown to users | < 2% of published websites |
| Website detail page load (p95) | < 1.5 s |
| Published relations without provenance | 0 |
| Rejected community contributions (spam rate) | tracked from Phase 23, alert if > 40% |

### 6.4 Anti-metrics

We will **not** optimise for these, and we will not report them as success:

- Total page views
- Total number of websites in the database
- Time on site as a single number (a lost user also spends a long time)
- Signup count without any exploring behaviour

---

## 7. Event names — decided now

The source document asks us to design event names in Phase 1, even though analytics is built in
Phase 34. This stops us from inventing names randomly later.

**Rules:** `snake_case`, `object_action` order, always lower case, never renamed after release.

| Event | When it fires | Key properties |
|---|---|---|
| `session_start` | First activity of a session | `is_authenticated`, `referrer` |
| `search_performed` | User submits a search | `query_length`, `result_count` |
| `search_result_click` | User opens a search result | `entity_type`, `position` |
| `node_view` | Any website, topic or technology page is viewed | `entity_type`, `entity_id`, `source` |
| `relation_click` | User moves along a relation — **the North Star event** | `relation_type`, `from_id`, `to_id` |
| `filter_apply` | User applies a filter | `filter_type`, `value_count` |
| `bookmark_add` | User saves an item | `entity_type` |
| `collection_create` | User creates a collection | `visibility` |
| `path_start` | User starts an exploration path | `path_id` |
| `path_complete` | User finishes all steps of a path | `path_id`, `duration` |
| `atlas_create` | User creates a personal atlas | `node_count` |
| `contribution_submit` | User sends a proposal | `contribution_type` |
| `external_link_click` | User opens the real website | `entity_id` |

`external_link_click` is interesting: it is both a success (we helped) and a risk (we lost them).
We track it, but it is **not** a success metric on its own.

---

## 8. MVP scope decision

The MVP is the smallest product that can prove the North Star Metric works.

**In the MVP (P0):** website model, taxonomy, relation graph, admin panel, seed data,
atlas map, website detail, topic pages, global search, plus auth and the technical base.

**Not in the MVP:** bookmarks, collections, paths, recommendations, community contributions,
crawler, AI, extension, public API.

**Why this line:** the MVP must answer one question — *do people actually explore the graph?*
Saving and personalisation make people **come back**, but they do not prove **exploring** works.
We add them right after, in Phases 19–22.

One risk we accept: without bookmarks, our Input 4 (return rate) will look weak in the MVP.
That is expected and we will not panic about it.

---

## 9. MVP backlog with acceptance criteria

This closes the Phase 1 exit criteria: every MVP item has a testable definition of done.

| ID | Item | Acceptance criteria |
|---|---|---|
| AT-001 | PRD and scope | This document exists, and a new developer can answer "what are we building and what are we not building" from it alone |
| AT-002 | ADR: stack | Every major technology choice has a written reason and at least one rejected option |
| AT-003 | Monorepo + CI | A clean machine can run the project with one documented command; lint, typecheck and tests run in CI on every pull request |
| AT-004 | PostgreSQL + migrations | Fresh database + migrations + seed runs with one command and gives the same result every time |
| AT-005 | User and session model | A user can register, verify email, log in and log out; protected endpoints reject unauthenticated requests; tests prove it |
| AT-006 | Core entity schema | Website, Topic, Category and Technology exist with unique constraints; a duplicate domain cannot be created |
| AT-007 | Relation schema | A relation stores source, target, type, weight, confidence and provenance; duplicate edges are rejected; cycles are handled by rule |
| AT-008 | Admin auth + CRUD | An admin can create, edit, publish and archive every core entity; a non-admin gets 403; every change is written to the audit log |
| AT-009 | Seed import script | A JSON/CSV file imports ~160 websites and ~500 relations; running it twice does not create duplicates |
| AT-010 | Graph neighbours API | `GET /graph/neighbors/:id` returns neighbours with a depth and node limit, and responds under 300 ms with seed data |
| AT-011 | Atlas map MVP | A user can pan, zoom, select a node and open its neighbours, for 3 levels deep, staying usable at 100–300 nodes; mobile gets the list fallback |
| AT-012 | Website detail | The page answers "what is it, what area, what is it connected to, what are the alternatives" on one screen, and shows last verified date |
| AT-013 | Topic detail | A topic page shows child topics, featured websites and a topic graph, and never shows an empty screen |
| AT-014 | Global search | A 1–2 word query returns the right entity in the top 5 results, with the entity type visible on each result card |

---

## 10. Main risks

| Risk | Why it is dangerous | How we reduce it |
|---|---|---|
| Scope grows | 40 phases is long. Adding "just one more domain" kills focus. | The non-goal list in §4 and the four-domain limit in the vision |
| We drift back to a directory | Lists are much easier to build than graphs. | Guardrail question 5 at every phase exit; graph density is a tracked input metric |
| Empty graph at launch | A map with 20 nodes looks broken. | Phase 13 exit rule: ≥ 5 complete routes must work |
| Wrong data | The Builder persona leaves forever after one wrong fact. | Provenance and confidence on every relation from Phase 11 |
| Building for the wrong user | Optimising for experts makes the product too complex for learners. | The Learner is primary until data proves otherwise |

---

## 11. Phase 1 exit criteria

- [x] Primary persona defined with 7 concrete scenarios
- [x] Secondary persona defined with its own scenarios
- [x] Anti-persona written down
- [x] Persona matrix completed (come / do / get / return)
- [x] Non-goal list written
- [x] Product language fixed as Discover → Understand → Explore
- [x] North Star Metric defined exactly, with a metric tree and guardrails
- [x] Event names designed before any analytics code
- [x] MVP scope line drawn, with a reason
- [x] Every MVP backlog item has acceptance criteria

**Phase 1 is closed. Next: Phase 2 — User flows (screen inventory, state inventory).**

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-19 | First PRD. Primary persona set to The Learner. North Star Metric set to Weekly Exploring Users. |
