import asyncio
import json
from app.core.database import AsyncSessionLocal
from app.repositories.task_repo import TaskRepository
from app.services.crawl_service import CrawlService
from app.repositories.log_repo import LogRepository
from app.models.task import Task
from app.schemas.task import TaskStatus
import app.models.data  # Fix the Missing Model

async def main():
    async with AsyncSessionLocal() as session:
        task_repo = TaskRepository(session)
        log_repo = LogRepository(session)
        service = CrawlService(task_repo=task_repo, log_repo=log_repo)

        task = Task(
            name="Scrape Quotes Example",
            start_url="https://quotes.toscrape.com/",
            status=TaskStatus.ENABLED,
            cron_expr="0 0 * * *",
            parser_rules=json.dumps({
                "title": "css:title",
                "content": "css:.col-md-8"
            }),
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        print(f'Created task {task.id}')

        await service.run_task(task.id)
        print('Task finished running!')

asyncio.run(main())
