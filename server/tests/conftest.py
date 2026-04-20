import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.models_base import Base


@pytest.fixture(scope="session")
def asgi_test_client() -> TestClient:
    """Single ASGI lifespan for the whole suite (APScheduler binds one event loop)."""
    from main import app

    with TestClient(app) as client:
        yield client


def pytest_configure() -> None:
    """Ensure app imports (e.g. HTTP smoke) use an isolated DB file under server/."""
    if os.environ.get("CRAWLER_DATABASE_URL"):
        return
    os.environ["CRAWLER_DATABASE_URL"] = "sqlite:///./_pytest_crawler.db"
    from app.core.config import get_settings

    get_settings.cache_clear()


def _import_models() -> None:
    from app.models.auth import User, UserSession  # noqa: F401
    from app.models.data import CollectedData  # noqa: F401
    from app.models.keyword_rule import KeywordRule  # noqa: F401
    from app.models.log import LogEntry  # noqa: F401
    from app.models.task import Task  # noqa: F401


@pytest.fixture
async def async_session() -> AsyncSession:
    _import_models()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
    await engine.dispose()
