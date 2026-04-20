import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.models_base import Base
from app.core.runtime_status import get_runtime_snapshot


def _import_models() -> None:
    from app.models.auth import User, UserSession  # noqa: F401
    from app.models.data import CollectedData  # noqa: F401
    from app.models.keyword_rule import KeywordRule  # noqa: F401
    from app.models.log import LogEntry  # noqa: F401
    from app.models.task import Task  # noqa: F401


@pytest.mark.asyncio
async def test_runtime_snapshot_with_memory_session_factory() -> None:
    _import_models()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        snap = await get_runtime_snapshot(session_factory=factory)
        assert snap["database"] == "ok"
        assert snap["scheduler"] in ("running", "stopped")
        assert snap["status"] in ("ok", "degraded")
    finally:
        await engine.dispose()
