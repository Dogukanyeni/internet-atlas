# Database

| Folder | Content |
|---|---|
| `migrations/` | Alembic migrations. Set up in Phase 7. |
| `seeds/` | Seed data for the first Atlas (Phase 13). |
| `fixtures/` | Fixed data used by tests. |

Rules:

- Every schema change is a migration. Never edit a database by hand.
- Every migration has a working downgrade.
- `make setup` plus migrations plus seed must give the same result every time.
