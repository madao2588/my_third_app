from collections.abc import AsyncGenerator
from pathlib import Path
import sys

try:
    import sqlite3  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - environment-specific fallback
    import pysqlite3 as sqlite3

    sys.modules["sqlite3"] = sqlite3

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


settings = get_settings()
server_dir = Path(__file__).resolve().parents[2]


def _build_async_database_url(database_url: str) -> str:
    async_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    prefix = "sqlite+aiosqlite:///"
    if async_url.startswith(prefix) and not async_url.startswith(f"{prefix}/"):
        relative_path = async_url.removeprefix(prefix)
        absolute_path = (server_dir / relative_path).resolve()
        return f"{prefix}{absolute_path.as_posix()}"
    return async_url


async_database_url = _build_async_database_url(settings.database_url)

engine = create_async_engine(async_database_url, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    # Import models here so metadata is fully populated before table creation.
    from app.models.auth import User, UserSession  # noqa: F401
    from app.models.data import CollectedData  # noqa: F401
    from app.models.log import LogEntry  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.keyword_rule import KeywordRule  # noqa: F401
    from app.models.keyword_rule import KeywordRule  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await _migrate_task_table(connection)


async def _migrate_task_table(connection) -> None:
    result = await connection.execute(text("PRAGMA table_info(tasks)"))
    existing_columns = {row[1] for row in result.fetchall()}
    required_columns = {
        "last_run_status": "TEXT",
        "last_run_at": "DATETIME",
        "last_success_at": "DATETIME",
        "last_error_message": "TEXT",
    }
    for column_name, column_type in required_columns.items():
        if column_name in existing_columns:
            continue
        await connection.execute(
            text(f"ALTER TABLE tasks ADD COLUMN {column_name} {column_type}")
        )


async def close_db() -> None:
    await engine.dispose()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
