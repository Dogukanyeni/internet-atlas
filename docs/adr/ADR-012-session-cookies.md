# ADR-012 — Session cookies with opaque tokens, not JWT in storage

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4
**Confirmed in detail in:** Phase 8

## Context

The frontend and the API are two separate applications. Next.js server components also call the
API from the server, so whatever we choose must work in three places: the browser, the Next.js
server, and direct API calls.

The source document lists "storing tokens in the wrong place" as a main risk of Phase 8, and
Phase 36 lists XSS as a top threat. This decision belongs to architecture, not to feature work.

## Decision

- The API issues an **opaque session token** (random, meaningless by itself).
- It is delivered in a cookie: **httpOnly, Secure, SameSite=Lax**, scoped to the parent domain so
  both `www.` and `api.` can use it.
- The session record lives in PostgreSQL, with a Redis lookup cache.
- **JavaScript never reads the token.** There is no token in `localStorage` or `sessionStorage`.
- Next.js server components **forward the incoming cookie** when they call the API.
- Logout deletes the session record, so it stops working immediately.

## Alternatives considered

| Option | Why rejected |
|---|---|
| JWT in `localStorage` | The most common pattern in tutorials and the easiest to steal: any XSS reads it instantly. Rejected outright. |
| JWT in an httpOnly cookie | Safe from XSS, and needs no session lookup. Rejected because a JWT cannot be revoked before it expires. We need instant logout, instant ban, and instant role change for moderation (Phase 24). |
| OAuth social login only | Fewer passwords to protect, but it makes an external provider a hard dependency for signing in at all. It can be added later next to email login. |

## Consequences

**Good**

- XSS cannot steal the session.
- Logout, ban and role changes take effect immediately.
- Sessions can be listed and revoked per device.

**Cost**

- Every authenticated request needs a session lookup. Redis caching keeps this cheap.
- Cookies across subdomains need correct CORS setup and `credentials: include`. This must be
  right in local, preview and production, and it is a common source of confusing bugs.
- `SameSite=Lax` requires care if we ever accept cross-site POST requests. We do not plan to.
- The public API (Phase 33) will **not** use cookies. It uses API keys, which is a separate
  mechanism by design.

## Revisit when

We add a mobile app or another non-browser client that cannot use cookies. Then a token-based
flow is added next to sessions, not instead of them.
