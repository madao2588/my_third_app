from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import asc, desc, func, nullsfirst, nullslast, or_, select, update
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
        search: str | None = None,
        enabled: str | None = None,
        last_run: str | None = None,
        sort_by: str | None = None,
        sort_dir: str | None = None,
    ) -> tuple[Sequence[Task], int]:
        filters: list = []
        needle = (search or "").strip()
        if needle:
            n = needle.lower()
            filters.append(
                or_(
                    func.lower(Task.name).contains(n),
                    func.lower(Task.start_url).contains(n),
                    func.lower(Task.cron_expr).contains(n),
                )
            )

        en = (enabled or "all").strip().lower()
        if en == "enabled":
            filters.append(Task.status == int(TaskStatus.ENABLED))
        elif en == "disabled":
            filters.append(Task.status == int(TaskStatus.DISABLED))

        lr = (last_run or "all").strip().lower()
        if lr == "success":
            filters.append(Task.last_run_status == "success")
        elif lr == "failed":
            filters.append(Task.last_run_status == "failed")
        elif lr == "active":
            filters.append(Task.last_run_status.in_(("queued", "running")))
        elif lr == "never":
            filters.append(
                or_(Task.last_run_status.is_(None), Task.last_run_status == "")
            )

        total_statement = select(func.count()).select_from(Task)
        if filters:
            total_statement = total_statement.where(*filters)
        total = await self.session.scalar(total_statement) or 0

        sb = (sort_by or "id").strip().lower()
        sd = (sort_dir or "desc").strip().lower()
        if sb not in {"id", "name", "last_run_at", "created_at"}:
            sb = "id"
        if sd not in {"asc", "desc"}:
            sd = "desc"

        if sb == "name":
            primary = Task.name
        elif sb == "last_run_at":
            primary = Task.last_run_at
        elif sb == "created_at":
            primary = Task.created_at
        else:
            primary = Task.id

        if sb == "last_run_at" and sd == "desc":
            order_cols = [nullslast(desc(primary)), desc(Task.id)]
        elif sb == "last_run_at" and sd == "asc":
            order_cols = [nullsfirst(asc(primary)), asc(Task.id)]
        elif sd == "asc":
            order_cols = [asc(primary), asc(Task.id)]
        else:
            order_cols = [desc(primary), desc(Task.id)]

        statement = select(Task)
        if filters:
            statement = statement.where(*filters)
        statement = statement.order_by(*order_cols).offset((page - 1) * page_size).limit(page_size)
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

    async def try_mark_run_queued(
        self,
        task_id: int,
        *,
        run_at: datetime,
    ) -> bool:
        """Atomically set ``queued`` if not already ``running`` or ``queued``."""
        status = func.coalesce(Task.last_run_status, "")
        stmt = (
            update(Task)
            .where(Task.id == task_id, status.notin_(("running", "queued")))
            .values(
                last_run_status="queued",
                last_run_at=run_at,
                last_error_message=None,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return (getattr(result, "rowcount", None) or 0) > 0

    async def try_mark_running(
        self,
        task_id: int,
        *,
        run_at: datetime,
    ) -> bool:
        """Atomically move into ``running`` unless already ``running`` (cross-worker safe)."""
        status = func.coalesce(Task.last_run_status, "")
        stmt = (
            update(Task)
            .where(Task.id == task_id, status != "running")
            .values(
                last_run_status="running",
                last_run_at=run_at,
                last_error_message=None,
            )
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return (getattr(result, "rowcount", None) or 0) > 0

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
