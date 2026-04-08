from collections.abc import Sequence

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log import LogEntry


class LogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        level: str,
        message: str,
        task_id: int | None = None,
        error_stack: str | None = None,
    ) -> LogEntry:
        log = LogEntry(
            task_id=task_id,
            level=level,
            message=message,
            error_stack=error_stack,
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def list_paginated(
        self,
        *,
        page: int,
        page_size: int,
        task_id: int | None = None,
        level: str | None = None,
    ) -> tuple[Sequence[LogEntry], int]:
        filters = []
        if task_id is not None:
            filters.append(LogEntry.task_id == task_id)
        if level is not None:
            filters.append(LogEntry.level == level)

        total_statement = select(func.count()).select_from(LogEntry)
        if filters:
            total_statement = total_statement.where(*filters)
        total = await self.session.scalar(total_statement) or 0

        statement = (
            select(LogEntry)
            .where(*filters)
            .order_by(LogEntry.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.execute(statement)
        return result.scalars().all(), total

    async def count_all(self) -> int:
        statement = select(func.count()).select_from(LogEntry)
        return await self.session.scalar(statement) or 0

    async def count_by_level(self, level: str) -> int:
        statement = select(func.count()).select_from(LogEntry).where(LogEntry.level == level)
        return await self.session.scalar(statement) or 0

    async def count_failed_tasks(self) -> int:
        statement = (
            select(func.count(distinct(LogEntry.task_id)))
            .select_from(LogEntry)
            .where(LogEntry.level == "ERROR", LogEntry.task_id.is_not(None))
        )
        return await self.session.scalar(statement) or 0
