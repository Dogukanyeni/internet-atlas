"""Health endpoints.

Three endpoints, because they answer three different questions (Phase 35 needs all of
them, and hosting platforms expect them):

* /health/live   — is the process running at all?
* /health/ready  — can it serve traffic? (database and redis reachable)
* /health/info   — what version is deployed?
"""

from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import text

from atlas.core import redis as redis_module
from atlas.core.config import get_settings
from atlas.core.db import engine
from atlas.core.logging import get_logger

router = APIRouter(prefix="/health", tags=["health"])
logger = get_logger(__name__)


class LiveResponse(BaseModel):
    status: Literal["ok"]


class DependencyStatus(BaseModel):
    database: bool
    redis: bool


class ReadyResponse(BaseModel):
    status: Literal["ready", "degraded"]
    dependencies: DependencyStatus


class InfoResponse(BaseModel):
    name: str
    version: str
    environment: str


async def _database_ok() -> bool:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning("readiness_database_failed", error=str(exc))
        return False
    return True


@router.get("/live", response_model=LiveResponse)
async def live() -> LiveResponse:
    return LiveResponse(status="ok")


@router.get("/ready", response_model=ReadyResponse)
async def ready(response: Response) -> ReadyResponse:
    database_ok = await _database_ok()
    redis_ok = await redis_module.ping()

    # The database is required. Redis is not: without it we are slower, not broken
    # (ADR-007), so a missing Redis reports "degraded" but still returns 200.
    if not database_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return ReadyResponse(
        status="ready" if database_ok and redis_ok else "degraded",
        dependencies=DependencyStatus(database=database_ok, redis=redis_ok),
    )


@router.get("/info", response_model=InfoResponse)
async def info() -> InfoResponse:
    settings = get_settings()
    return InfoResponse(name="internet-atlas-api", version="0.1.0", environment=settings.env.value)
