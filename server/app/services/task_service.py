from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.scheduler import get_scheduler
from app.models.task import Task
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.common import EmptyPayload, PageData
from app.schemas.task import TaskCreate, TaskRead, TaskRunPayload, TaskStatus, TaskUpdate
from app.services.crawl_service import CrawlService, dispatch_task_run


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        log_repo: LogRepository,
        crawl_service: CrawlService,
        scheduler: AsyncIOScheduler | None = None,
    ):
        self.task_repo = task_repo
        self.log_repo = log_repo
        self.crawl_service = crawl_service
        self.scheduler = scheduler or get_scheduler()

    async def list_tasks(self, *, page: int, page_size: int) -> PageData[TaskRead]:
        items, total = await self.task_repo.list_paginated(page=page, page_size=page_size)
        return PageData[TaskRead](
            items=[TaskRead.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_task(self, task_id: int) -> TaskRead:
        task = await self._get_task_or_raise(task_id)
        return TaskRead.model_validate(task)

    async def create_task(self, payload: TaskCreate) -> TaskRead:
        self._validate_cron_expr(payload.cron_expr)
        task = await self.task_repo.create(payload)
        await self._sync_scheduler(task)
        await self.log_repo.create(
            level="INFO",
            task_id=task.id,
            message=f"Task {task.id} created",
        )
        return TaskRead.model_validate(task)

    async def update_task(self, task_id: int, payload: TaskUpdate) -> TaskRead:
        task = await self._get_task_or_raise(task_id)
        update_data = payload.model_dump(exclude_unset=True)
        cron_expr = update_data.get("cron_expr")
        if cron_expr is not None:
            self._validate_cron_expr(cron_expr)

        updated_task = await self.task_repo.update(task, payload)
        await self._sync_scheduler(updated_task)
        await self.log_repo.create(
            level="INFO",
            task_id=updated_task.id,
            message=f"Task {updated_task.id} updated",
        )
        return TaskRead.model_validate(updated_task)

    async def delete_task(self, task_id: int) -> EmptyPayload:
        task = await self._get_task_or_raise(task_id)
        self._remove_job(task.id)
        await self.task_repo.delete(task)
        await self.log_repo.create(
            level="INFO",
            task_id=None,
            message=f"Task {task_id} deleted",
        )
        return EmptyPayload()

    async def run_task_now(self, task_id: int) -> TaskRunPayload:
        await self._get_task_or_raise(task_id)
        return await self.crawl_service.trigger_now(task_id)

    async def load_enabled_tasks(self) -> None:
        enabled_tasks = await self.task_repo.list_enabled()
        for task in enabled_tasks:
            try:
                await self._sync_scheduler(task)
            except ValueError as exc:
                await self.log_repo.create(
                    level="ERROR",
                    task_id=task.id,
                    message=f"Failed to load scheduled task {task.id}",
                    error_stack=str(exc),
                )

    async def ensure_example_task(self) -> TaskRead | None:
        if await self.task_repo.count_all() > 0:
            return None

        example = TaskCreate(
            name="Example News Task",
            start_url="https://example.com",
            parser_rules=None,
            cron_expr="0 */6 * * *",
            status=TaskStatus.ENABLED,
        )
        return await self.create_task(example)

    async def _sync_scheduler(self, task: Task) -> None:
        if int(task.status) != int(TaskStatus.ENABLED):
            self._remove_job(task.id)
            return

        trigger = CronTrigger.from_crontab(task.cron_expr)
        self.scheduler.add_job(
            dispatch_task_run,
            trigger=trigger,
            args=[task.id],
            id=self._job_id(task.id),
            replace_existing=True,
            coalesce=True,
        )

    async def _get_task_or_raise(self, task_id: int) -> Task:
        task = await self.task_repo.get_by_id(task_id)
        if task is None:
            raise LookupError(f"Task {task_id} not found")
        return task

    def _validate_cron_expr(self, cron_expr: str) -> None:
        CronTrigger.from_crontab(cron_expr)

    def _remove_job(self, task_id: int) -> None:
        try:
            self.scheduler.remove_job(self._job_id(task_id))
        except JobLookupError:
            return

    def _job_id(self, task_id: int) -> str:
        return f"task_{task_id}"
