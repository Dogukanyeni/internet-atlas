"""Database engine and session.

Phase 7 adds models, migrations and repositories. This file only creates the connection,
so the readiness check has something real to test.

Rule from ADR-006: lazy loading is off. Relationships must be loaded on purpose with
`selectinload`, or the code raises instead of silently making extra queries.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from atlas.core.config import get_settings

_settings = get_settings()

engine: AsyncEngine = create_async_engine(
    _settings.database_url.get_secret_value(),
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency. One session per request, always closed."""
    async with SessionFactory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
