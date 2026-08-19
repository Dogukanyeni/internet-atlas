# ADR-003 — Next.js (App Router) for the frontend

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

The product has two very different kinds of screen:

1. **Content pages** — topic and website pages. These need search engine visibility, because
   organic search on topic names is our main discovery channel.
2. **The Atlas map** — a heavy interactive graph with pan, zoom, selection and progressive
   loading. This is a client application.

One framework must handle both well.

## Decision

**Next.js with the App Router**, TypeScript, React.

- Topic, website, technology and category pages are **server rendered** with caching.
- The map is a **client component**, loaded lazily, never server rendered.
- Route handlers are used only for small frontend-owned needs (for example the anonymous id
  cookie). All product data comes from the FastAPI API.

## Alternatives considered

| Option | Why rejected |
|---|---|
| React Router v7 / Remix | A cleaner mental model and very good data loading. Rejected for the smaller ecosystem around graph rendering and performance work, which is exactly where we will need existing answers in Phase 14. |
| Astro with React islands | The best possible content pages, but the map is a full interactive app, which is the case Astro is least suited to. |
| Plain React SPA (Vite) | Simplest for the map, but no server rendering. Topic pages would be invisible to search engines, which removes our main growth channel. |
| Server rendering from FastAPI templates | One less app to run, but the map would then need a separate build anyway, and we lose the React ecosystem. |

## Consequences

**Good**

- SEO works for content pages without extra work.
- The map gets a full client environment with no compromise.
- Large ecosystem for the graph libraries we will evaluate in Phase 14.

**Cost**

- The App Router has real complexity: caching layers, server versus client components, and
  cookie forwarding during server-side fetches.
- Two servers must be deployed and kept in the same region, or server rendering pays double
  network latency.
- Rule to prevent a common mistake: **server components must forward the session cookie** when
  they call the API, or logged-in users will see anonymous pages.

## Revisit when

Server rendering costs more than it returns — for example if most traffic turns out to be logged
in and personalised, which would make caching useless.
