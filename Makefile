# Internet Atlas — one entry point for every command.
# Works in Git Bash on Windows, and on macOS/Linux.
# Rule: if a task needs more than one command, it belongs here.

.DEFAULT_GOAL := help
.PHONY: help setup up down logs api web worker test test-api test-web lint format typecheck openapi check clean reset

API := apps/api
WEB := apps/web

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## First-time setup: install all dependencies and create .env
	@test -f .env || (cp .env.example .env && echo "Created .env from .env.example")
	cd $(API) && uv sync --all-extras
	pnpm install
	uv run --directory $(API) pre-commit install --install-hooks
	uv run --directory $(API) pre-commit install --hook-type commit-msg
	@echo ""
	@echo "Setup finished. Next: make up && make api"

up: ## Start Postgres, Redis and MinIO
	docker compose up -d
	@echo "Waiting for services to be healthy..."
	@docker compose ps

down: ## Stop the local services
	docker compose down

logs: ## Follow the service logs
	docker compose logs -f

api: ## Run the API at http://localhost:8000
	cd $(API) && uv run uvicorn atlas.main:app --reload --port 8000

worker: ## Run the background worker
	cd $(API) && uv run arq atlas.jobs.worker.WorkerSettings

web: ## Run the web app at http://localhost:3000
	pnpm --filter @atlas/web dev

test: test-api test-web ## Run every test

test-api: ## Run backend tests
	cd $(API) && uv run pytest -q

test-web: ## Run frontend tests
	pnpm --filter @atlas/web test --if-present

lint: ## Check code style in both languages
	cd $(API) && uv run ruff check .
	cd $(API) && uv run ruff format --check .
	pnpm --filter @atlas/web lint

format: ## Fix code style automatically
	cd $(API) && uv run ruff check --fix .
	cd $(API) && uv run ruff format .
	pnpm --filter @atlas/web lint --fix

typecheck: ## Type check both languages
	cd $(API) && uv run mypy src
	pnpm --filter @atlas/web typecheck

openapi: ## Write the OpenAPI schema used to generate the TypeScript client (ADR-011)
	cd $(API) && uv run python -m atlas.scripts.export_openapi ../../packages/api-client/openapi.json

check: lint typecheck test ## Everything CI runs, locally

clean: ## Remove build output and caches
	rm -rf $(WEB)/.next $(API)/.pytest_cache $(API)/.mypy_cache $(API)/.ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true

reset: ## Delete local data and start the services fresh (destroys the local database)
	docker compose down -v
	docker compose up -d
