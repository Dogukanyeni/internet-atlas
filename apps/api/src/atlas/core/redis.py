"""Redis client.

One instance serves cache, rate limits and the job queue, separated by key prefix
(ADR-007). The prefixes live here so they cannot drift apart across modules.

Rule: everything stored in Redis is disposable. If Redis is empty, the product still
works, only slower. Nothing lives here and nowhere else.
"""

from typing import Final

import redis.asyncio as aioredis

from atlas.core.config import get_settings

CACHE_PREFIX: Final = "cache:"
RATE_LIMIT_PREFIX: Final = "rl:"
CRAWL_PREFIX: Final = "crawl:domain:"
SESSION_PREFIX: Final = "sess:"

_settings = get_settings()

# redis-py ships no type information for the async `from_url` helper.
redis_client: aioredis.Redis = aioredis.from_url(  # type: ignore[no-untyped-call]
    _settings.redis_url.get_secret_value(),
    encoding="utf-8",
    decode_responses=True,
    health_check_interval=30,
)


async def ping() -> bool:
    """Used by the readiness check. Never raises."""
    try:
        return bool(await redis_client.ping())
    except Exception:
        return False
