# Local setup

Goal: a clean machine runs the whole project with a few commands.
If any step here does not work, that is a bug in this document — fix the document.

---

## 1. Install the tools

You already have git, Python 3.12 and Node 24. You still need three things.

### Docker Desktop

Download and install: <https://www.docker.com/products/docker-desktop/>

It will ask to enable WSL 2. Say yes and restart when it asks. After restart, check:

```bash
docker --version
```

### uv (Python package manager)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal, then check:

```bash
uv --version
```

### pnpm (Node package manager)

```bash
npm install -g pnpm
```

Check:

```bash
pnpm --version
```

---

## 2. Set up the project

```bash
cd C:/Internet_Atlas
make setup
```

This installs Python and Node dependencies, creates `.env` from `.env.example`, and
installs the git hooks.

**Then open `.env` and change one value:**

```
ATLAS_SECRET_KEY=<a long random string, at least 32 characters>
```

The API refuses to start with the placeholder value. That is on purpose.

---

## 3. Start the services

```bash
make up
```

This starts three containers:

| Service | Port | What it is |
|---|---|---|
| PostgreSQL | **5433** | The database (5433 on purpose, see below) |
| Redis | 6379 | Cache, rate limits, job queue |
| MinIO | 9000 / 9001 | S3-compatible file storage (console on 9001) |

Check they are healthy:

```bash
docker compose ps
```

---

## 4. Run the applications

Each one needs its own terminal.

```bash
make api      # http://localhost:8000
make web      # http://localhost:3000
make worker   # background jobs (not needed until Phase 26)
```

**Check it works:**

- <http://localhost:8000/health/live> → `{"status":"ok"}`
- <http://localhost:8000/health/ready> → shows database and redis as `true`
- <http://localhost:8000/docs> → the API documentation
- <http://localhost:3000> → the placeholder page, showing `API: connected`

---

## 5. Daily commands

```bash
make            # list every command
make check      # lint + typecheck + tests, same as CI
make format     # fix code style automatically
make test       # run tests
make openapi    # regenerate the API schema after changing models
make down       # stop the services
make reset      # delete local data and start fresh
```

---

## Problems and fixes

**`make: command not found`**
Use Git Bash, not PowerShell. Make comes with Git for Windows.

**`docker: command not found` after installing Docker Desktop**
Docker Desktop must be running. Open it and wait for the whale icon to stop moving.

**Why is PostgreSQL on 5433 and not 5432?**
Because a native PostgreSQL installed on Windows usually owns 5432, and Docker will
happily publish the port anyway. Your app then connects to the *wrong* database and the
error looks nothing like the cause - normally `password authentication failed`. Using
5433 removes the whole class of problem and leaves any native PostgreSQL untouched.

To check what owns a port:

```powershell
Get-NetTCPConnection -LocalPort 5432 -State Listen | ForEach-Object { (Get-Process -Id $_.OwningProcess).ProcessName }
```

**`password authentication failed for user "atlas"`**
Something other than our container is answering on that port. See the note above, and
make sure `DATABASE_URL` in `.env` uses port **5433**.

**The API says `ATLAS_SECRET_KEY must be at least 32 characters`**
Open `.env` and set a real value. Generate one:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

**`make api` says the database is not reachable**
Run `make up` first, and wait a few seconds for PostgreSQL to become healthy.
Check it directly:

```bash
docker compose exec postgres psql -U atlas -d atlas -c "select 1"
```

**The test database is missing**
Tests use a separate `atlas_test` database. It is created automatically when the
postgres volume is built for the first time. If your volume already existed, create it
once by hand:

```bash
docker compose exec postgres psql -U atlas -d atlas -c "CREATE DATABASE atlas_test OWNER atlas;"
```

**Line ending warnings in git**
Expected on Windows. `.editorconfig` and the pre-commit hooks keep files as LF.
