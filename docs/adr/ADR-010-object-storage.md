# ADR-010 — S3-compatible object storage for files

**Status:** Accepted · **Date:** 2026-08-19 · **Phase:** 4

## Context

We store binary files: website logos, screenshots, and later raw crawler responses and page
snapshots (Phases 26 and 29). Raw crawl artifacts can grow quickly and are mostly written once
and read rarely.

## Decision

Use **S3-compatible object storage** through the standard S3 API, so any provider works
(Cloudflare R2, Backblaze B2, AWS S3, MinIO locally).

**Bucket layout:**

| Prefix | Content | Public? | Retention |
|---|---|---|---|
| `logos/` | Website logos, processed sizes | Yes, via CDN | Forever |
| `shots/` | Screenshots | Yes, via CDN | Forever, replaced on refresh |
| `raw/` | Raw crawl responses | **No** | 90 days, then deleted |
| `snap/` | Page snapshots for change tracking | **No** | 12 months |

**Rules:**

- The database stores the **key**, never a full URL. Provider or domain changes must not require
  a data migration.
- Public files are served through a CDN, never straight from the API.
- Uploads from the admin panel use pre-signed URLs, so file bytes never pass through the API.
- Every uploaded image is validated by real content type and size, not by file extension. This is
  a Phase 36 security requirement, written here so it is designed in, not added later.

## Alternatives considered

| Option | Why rejected |
|---|---|
| Files in PostgreSQL (`bytea`) | Simple at first, but it makes backups huge and slow, and blocks CDN delivery. |
| Local disk on the server | Breaks with more than one instance, and disappears on redeploy with managed hosting. |
| A provider-specific SDK and features | Faster to start, but locks us to one host, against [ADR-013](ADR-013-managed-hosting.md). |

## Consequences

**Good**

- Cheap, scalable, and portable between providers.
- Raw crawl data can grow without touching database size or backup time.
- Retention rules keep storage cost predictable.

**Cost**

- One more service in local development. MinIO in Docker Compose solves it, and a local folder
  works as a fallback.
- Cleaning old objects needs a scheduled job, which becomes a small part of Phase 26.

## Revisit when

Storage cost becomes noticeable — most likely from `raw/`. The first fix is shorter retention or
compression, not a new provider.
