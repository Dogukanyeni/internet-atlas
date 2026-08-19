"""FastAPI application entry point.

This is the modular monolith from ADR-001. Modules are mounted here and nowhere else,
so one file always shows the whole API surface.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from atlas.core.config import Environment, get_settings
from atlas.core.db import engine
from atlas.core.errors import register_error_handlers
from atlas.core.logging import RequestIdMiddleware, configure_logging, get_logger
from atlas.core.redis import redis_client
from atlas.modules.health.router import router as health_router

settings = get_settings()
configure_logging(json_output=settings.env is not Environment.LOCAL)
logger = get_logger(__name__)

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("api_starting", environment=settings.env.value)
    yield
    await engine.dispose()
    await redis_client.aclose()
    logger.info("api_stopped")


app = FastAPI(
    title="Internet Atlas API",
    version="0.1.0",
    description="Discovery platform for the technology ecosystem.",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,  # session cookie must travel (ADR-012)
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "X-Request-ID"],
)

register_error_handlers(app)

# --- Modules -----------------------------------------------------------------
# Health is not versioned: platforms and monitors expect a stable path.
app.include_router(health_router)

# Product modules are added here as their phases arrive:
#   catalog  (Phase 9)    taxonomy (Phase 10)   graph  (Phase 11)
#   auth     (Phase 8)    search   (Phase 17)   admin  (Phase 12)
