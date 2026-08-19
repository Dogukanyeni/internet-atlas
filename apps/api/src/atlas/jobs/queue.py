"""The only way the application enqueues work.

ADR-008: no module imports arq directly. Everything goes through this file, so
replacing arq later touches one module instead of the whole codebase.
"""

from datetime import datetime
from typing import Any

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from atlas.core.config import get_settings
from atlas.core.logging import get_logger

logger = get_logger(__name__)

_pool: ArqRedis | None = None


def redis_settings() -> RedisSettings:
    settings = get_settings()
    return RedisSettings.from_dsn(settings.redis_url.get_secret_value())


async def get_pool() -> ArqRedis:
    global _pool  # noqa: PLW0603 - one pool per process is intended
    if _pool is None:
        _pool = await create_pool(redis_settings())
    return _pool


async def enqueue(
    job_name: str,
    *,
    payload: dict[str, Any] | None = None,
    run_at: datetime | None = None,
    job_id: str | None = None,
) -> str | None:
    """Put one job on the queue.

    `job_id` makes the call idempotent: enqueueing the same id twice runs it once.
    Phase 28 relies on this for the enrichment pipeline.
    """
    pool = await get_pool()
    job = await pool.enqueue_job(job_name, payload or {}, _defer_until=run_at, _job_id=job_id)
    if job is None:
        logger.info("job_already_queued", job_name=job_name, job_id=job_id)
        return None
    logger.info("job_enqueued", job_name=job_name, job_id=job.job_id)
    return job.job_id
