from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskStatus, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: TaskCreate) -> Task:
        task = Task(**payload.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: int) -> Task | None:
        statement = select(Task).where(Task.id == task_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_paginated(
        self,
        *,
        page: int,
        page_size: int,
    ) -> tuple[Sequence[Task], int]:
        total = await self.count_all()
        statement = (
            select(Task)
            .order_by(Task.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.execute(statement)
        return result.scalars().all(), total

    async def list_enabled(self) -> Sequence[Task]:
        statement = (
            select(Task)
            .where(Task.status == int(TaskStatus.ENABLED))
            .order_by(Task.id.asc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update(self, task: Task, payload: TaskUpdate) -> Task:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_run_state(
        self,
        task: Task,
        *,
        last_run_status: str,
        last_run_at: datetime | None = None,
        last_success_at: datetime | None = None,
        last_error_message: str | None = None,
    ) -> Task:
        task.last_run_status = last_run_status
        if last_run_at is not None:
            task.last_run_at = last_run_at
        if last_success_at is not None:
            task.last_success_at = last_success_at
        task.last_error_message = last_error_message
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()

    async def count_all(self) -> int:
        statement = select(func.count()).select_from(Task)
        return await self.session.scalar(statement) or 0

    async def count_enabled(self) -> int:
        statement = select(func.count()).select_from(Task).where(
            Task.status == int(TaskStatus.ENABLED)
        )
        return await self.session.scalar(statement) or 0
