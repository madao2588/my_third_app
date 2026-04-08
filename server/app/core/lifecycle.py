from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.database import AsyncSessionLocal, close_db, init_db
from app.core.scheduler import get_scheduler
from app.repositories.auth_repo import AuthRepository
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.services.auth_service import AuthService
from app.services.crawl_service import CrawlService
from app.services.task_service import TaskService


settings = get_settings()
server_dir = Path(__file__).resolve().parents[2]


def ensure_runtime_directories() -> None:
    for relative_path in (settings.snapshot_dir, settings.export_dir):
        (server_dir / relative_path).mkdir(parents=True, exist_ok=True)


async def bootstrap_tasks() -> None:
    async with AsyncSessionLocal() as session:
        task_repo = TaskRepository(session)
        log_repo = LogRepository(session)
        crawl_service = CrawlService(task_repo=task_repo, log_repo=log_repo)
        task_service = TaskService(
            task_repo=task_repo,
            log_repo=log_repo,
            crawl_service=crawl_service,
        )
        await task_service.ensure_example_task()
        await task_service.load_enabled_tasks()


async def bootstrap_auth() -> None:
    async with AsyncSessionLocal() as session:
        auth_repo = AuthRepository(session)
        auth_service = AuthService(auth_repo=auth_repo)
        await auth_service.ensure_default_admin()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    ensure_runtime_directories()
    await init_db()
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.start()
    await bootstrap_auth()
    await bootstrap_tasks()
    try:
        yield
    finally:
        if scheduler.running:
            scheduler.shutdown(wait=False)
        await close_db()
