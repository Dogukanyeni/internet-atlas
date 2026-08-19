"""Shared test setup.

Environment variables are set before the app is imported, so tests never depend on a
real .env file and never touch a real database by accident.
"""

import os

os.environ.setdefault("ATLAS_ENV", "local")
os.environ.setdefault("ATLAS_DEBUG", "true")
os.environ.setdefault("ATLAS_SECRET_KEY", "test-secret-key-that-is-long-enough-123456")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://atlas:atlas@localhost:5432/atlas_test"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")

from collections.abc import AsyncGenerator  # noqa: E402

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from atlas.main import app  # noqa: E402


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    """An HTTP client that talks to the app in memory — no network, no server."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
