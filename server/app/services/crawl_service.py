import asyncio
from datetime import datetime, timezone
from importlib import import_module

from app.core.database import AsyncSessionLocal
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskRunPayload


class CrawlService:
    def __init__(self, task_repo: TaskRepository, log_repo: LogRepository):
        self.task_repo = task_repo
        self.log_repo = log_repo

    async def run_task(self, task_id: int) -> None:
        task = await self.task_repo.get_by_id(task_id)
        if task is None:
            await self.log_repo.create(
                level="ERROR",
                task_id=task_id,
                message=f"Task {task_id} not found for execution",
            )
            raise LookupError(f"Task {task_id} not found")

        await self.task_repo.update_run_state(
            task,
            last_run_status="running",
            last_run_at=datetime.now(timezone.utc),
            last_error_message=None,
        )

        pipeline_module = import_module("app.engine.pipeline")
        pipeline_runner = getattr(pipeline_module, "run_task", None)
        if not callable(pipeline_runner):
            await self.task_repo.update_run_state(
                task,
                last_run_status="idle",
                last_error_message="Pipeline runner is not implemented yet",
            )
            await self.log_repo.create(
                level="WARNING",
                task_id=task_id,
                message="Pipeline runner is not implemented yet",
            )
            return

        try:
            await pipeline_runner(task_id)
            refreshed_task = await self.task_repo.get_by_id(task_id)
            if refreshed_task is not None:
                await self.task_repo.update_run_state(
                    refreshed_task,
                    last_run_status="success",
                    last_success_at=datetime.now(timezone.utc),
                    last_error_message=None,
                )
            await self.log_repo.create(
                level="INFO",
                task_id=task_id,
                message=f"Task {task_id} execution finished",
            )
        except Exception as exc:
            failed_task = await self.task_repo.get_by_id(task_id)
            if failed_task is not None:
                await self.task_repo.update_run_state(
                    failed_task,
                    last_run_status="failed",
                    last_error_message=str(exc),
                )
            await self.log_repo.create(
                level="ERROR",
                task_id=task_id,
                message=f"Task {task_id} execution failed",
                error_stack=str(exc),
            )
            raise

    async def trigger_now(self, task_id: int) -> TaskRunPayload:
        task = await self.task_repo.get_by_id(task_id)
        if task is None:
            raise LookupError(f"Task {task_id} not found")

        await self.task_repo.update_run_state(
            task,
            last_run_status="queued",
            last_error_message=None,
        )
        asyncio.create_task(dispatch_task_run(task_id))
        return TaskRunPayload(task_id=task_id, status="queued")


async def dispatch_task_run(task_id: int) -> None:
    async with AsyncSessionLocal() as session:
        task_repo = TaskRepository(session)
        log_repo = LogRepository(session)
        service = CrawlService(task_repo=task_repo, log_repo=log_repo)
        await service.run_task(task_id)
