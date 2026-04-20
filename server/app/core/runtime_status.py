"""进程内运行态快照：数据库连通性、调度器。供 /health 与仪表盘等复用。"""

from __future__ import annotations

from typing import TypedDict

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import AsyncSessionLocal
from app.core.scheduler import get_scheduler


class RuntimeSnapshot(TypedDict):
    status: str
    database: str
    scheduler: str
    scheduled_jobs: int


async def get_runtime_snapshot(
    *,
    session_factory: async_sessionmaker[AsyncSession] | None = None,
) -> RuntimeSnapshot:
    database = "ok"
    factory = session_factory or AsyncSessionLocal
    try:
        async with factory() as session:
            await session.execute(text("SELECT 1"))
    except Exception:
        database = "error"

    scheduler_obj = get_scheduler()
    scheduler_state = "running" if scheduler_obj.running else "stopped"
    job_count = len(scheduler_obj.get_jobs()) if scheduler_obj.running else 0
    overall = "ok" if database == "ok" else "degraded"

    return RuntimeSnapshot(
        status=overall,
        database=database,
        scheduler=scheduler_state,
        scheduled_jobs=job_count,
    )
