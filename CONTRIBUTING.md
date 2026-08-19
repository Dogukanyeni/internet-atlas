# Contributing

These rules exist because the project has 40 phases. Without discipline, technical debt
arrives long before the product does.

---

## Branches

| Type | Name | Example |
|---|---|---|
| Feature | `feat/<phase>-<short-name>` | `feat/11-relation-graph` |
| Fix | `fix/<short-name>` | `fix/duplicate-domain-check` |
| Docs | `docs/<short-name>` | `docs/phase-6-contracts` |
| Chore | `chore/<short-name>` | `chore/upgrade-ruff` |

`main` is always deployable. Nobody pushes to `main` directly.

## Commits

Conventional commits, checked by a git hook:

```
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
Scope is usually the module: `graph`, `catalog`, `taxonomy`, `auth`, `web`, `ingest`.

Good: `feat(graph): add neighbours endpoint with depth limit`
Bad: `update stuff`

## Before you open a pull request

```bash
make check     # lint + typecheck + tests, the same as CI
```

If you changed API models, also run:

```bash
make openapi   # updates the schema; commit the result
```

CI fails if the committed schema does not match the code ([ADR-011](docs/adr/ADR-011-openapi-typed-client.md)).

---

## Definition of Ready

A task may only be started when:

- The user problem and value fit in one sentence.
- Acceptance criteria exist.
- If there is UI, the screens and states are listed.
- If the data model changes, a draft exists.
- Dependencies and risks are noted.

## Definition of Done

A task is finished when:

- Code is reviewed.
- Tests are written and pass in CI.
- Authorization and validation are in place.
- Loading, empty, error, unauthorized and archived states are handled.
- Logs, metrics or events are added where they will be needed.
- Documentation is updated.
- The migration has a working rollback.
- A production smoke test passes (once deployment exists).

---

## Code standards

### Both languages

- Names say what a thing is, not what type it is. `websites`, not `websiteList`.
- No commented-out code. Git remembers it.
- A comment explains **why**, never **what**. The code already says what.
- Delete dead code as soon as it is dead.

### Python

- Async first. One blocking call inside an async function stalls the whole event loop.
- Type hints everywhere. `mypy --strict` must pass for `src/`.
- Layer rules: routers do auth and validation, services hold business rules, repositories
  hold queries. A router that writes SQL is a bug.
- Never import another module's internals. Call its service layer.
- `print()` is not allowed. Use the logger.

### TypeScript

- No `any`. If a type is hard, model it properly.
- API types come only from `@atlas/api-client`. Never write an API interface by hand.
- Server components must forward the session cookie when they call the API, or logged-in
  users see anonymous pages ([ADR-003](docs/adr/ADR-003-nextjs.md)).

### Database

- Every change is a migration. No manual edits to a database.
- Every migration has a working downgrade.
- Indexes are added because of a real query, and the migration says which one.

### Security (from day one, not from Phase 36)

- Secrets only in environment variables. Never in code, never in a commit.
- Every external URL we fetch passes the SSRF policy (Phase 26).
- Every user input is validated at the API boundary.
- Errors shown to users never contain internal details.

---

## Tests

| Kind | What it covers |
|---|---|
| Unit | Scoring, relation validation, slug rules, permissions, parsers |
| Integration | Repository plus database, auth, queue jobs, search queries |
| Contract | The generated client matches the API schema |
| End to end | Onboarding, search, explore, save, return; admin edit and publish |
| Regression | Fixed examples for technology detection and AI classification |

A bug fix starts with a test that fails.
