"""Worker entry point.

Run with:  make worker

The worker shares the whole API codebase — same models, same services — but runs as a
separate process (ADR-001). Long work never happens inside a user request.
"""

from typing import Any

from atlas.core.config import Environment, get_settings
from atlas.core.logging import configure_logging, get_logger
from atlas.jobs.queue import redis_settings

settings = get_settings()
configure_logging(json_output=settings.env is not Environment.LOCAL)
logger = get_logger(__name__)


async def ping(_: dict[str, Any], payload: dict[str, Any]) -> str:
    """A job that does nothing, used to prove the queue works end to end."""
    logger.info("ping_job", payload=payload)
    return "pong"


async def startup(_: dict[str, Any]) -> None:
    logger.info("worker_starting", environment=settings.env.value)


async def shutdown(_: dict[str, Any]) -> None:
    logger.info("worker_stopped")


class WorkerSettings:
    """arq reads this class. Job functions are registered here as phases add them."""

    functions = [ping]  # noqa: RUF012 - arq expects a plain list
    cron_jobs: list[Any] = []  # noqa: RUF012 - filled from Phase 26 (freshness checks)

    on_startup = startup
    on_shutdown = shutdown

    redis_settings = redis_settings()

    max_jobs = 10
    job_timeout = 300  # seconds; a single job must never run longer
    max_tries = 3  # then it goes to failed_jobs in PostgreSQL (ADR-008)
    keep_result = 3600
