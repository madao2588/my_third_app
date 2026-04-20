from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from app.models.task import Task
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskStatus


@pytest.mark.asyncio
async def test_try_mark_running_second_claim_fails(async_session) -> None:
    async_session.add(
        Task(
            name="claim test",
            start_url="https://claim.example",
            cron_expr="0 * * * *",
            status=int(TaskStatus.ENABLED),
            last_run_status="queued",
        )
    )
    await async_session.commit()
    t = (await async_session.execute(select(Task).limit(1))).scalar_one()
    repo = TaskRepository(async_session)
    now = datetime.now(UTC)
    assert await repo.try_mark_running(t.id, run_at=now) is True
    assert await repo.try_mark_running(t.id, run_at=now) is False


@pytest.mark.asyncio
async def test_try_mark_run_queued_false_when_already_queued(async_session) -> None:
    async_session.add(
        Task(
            name="queue test",
            start_url="https://queue.example",
            cron_expr="0 * * * *",
            status=int(TaskStatus.ENABLED),
            last_run_status="queued",
        )
    )
    await async_session.commit()
    t = (await async_session.execute(select(Task).limit(1))).scalar_one()
    repo = TaskRepository(async_session)
    now = datetime.now(UTC)
    assert await repo.try_mark_run_queued(t.id, run_at=now) is False


@pytest.mark.asyncio
async def test_list_paginated_search_name(async_session) -> None:
    async_session.add_all(
        [
            Task(
                name="Alpha crawl",
                start_url="https://a.example",
                cron_expr="0 * * * *",
                status=int(TaskStatus.ENABLED),
            ),
            Task(
                name="Beta",
                start_url="https://b.example",
                cron_expr="0 * * * *",
                status=int(TaskStatus.ENABLED),
            ),
        ]
    )
    await async_session.commit()

    repo = TaskRepository(async_session)
    items, total = await repo.list_paginated(page=1, page_size=20, search="alpha")
    assert total == 1
    assert len(items) == 1
    assert items[0].name == "Alpha crawl"


@pytest.mark.asyncio
async def test_list_paginated_enabled_filter(async_session) -> None:
    async_session.add_all(
        [
            Task(
                name="On",
                start_url="https://on.example",
                cron_expr="* * * * *",
                status=int(TaskStatus.ENABLED),
            ),
            Task(
                name="Off",
                start_url="https://off.example",
                cron_expr="* * * * *",
                status=int(TaskStatus.DISABLED),
            ),
        ]
    )
    await async_session.commit()

    repo = TaskRepository(async_session)
    _, total_enabled = await repo.list_paginated(page=1, page_size=20, enabled="enabled")
    _, total_disabled = await repo.list_paginated(page=1, page_size=20, enabled="disabled")
    assert total_enabled == 1
    assert total_disabled == 1


@pytest.mark.asyncio
async def test_list_paginated_last_run_active(async_session) -> None:
    async_session.add_all(
        [
            Task(
                name="Running",
                start_url="https://r.example",
                cron_expr="* * * * *",
                status=1,
                last_run_status="running",
            ),
            Task(
                name="Done",
                start_url="https://d.example",
                cron_expr="* * * * *",
                status=1,
                last_run_status="success",
            ),
        ]
    )
    await async_session.commit()

    repo = TaskRepository(async_session)
    items, total = await repo.list_paginated(page=1, page_size=20, last_run="active")
    assert total == 1
    assert items[0].name == "Running"


@pytest.mark.asyncio
async def test_list_paginated_sort_last_run_at_desc_nulls_last(async_session) -> None:
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
    async_session.add_all(
        [
            Task(
                name="WithTime",
                start_url="https://t.example",
                cron_expr="* * * * *",
                status=1,
                last_run_at=base,
            ),
            Task(
                name="NoTime",
                start_url="https://n.example",
                cron_expr="* * * * *",
                status=1,
                last_run_at=None,
            ),
        ]
    )
    await async_session.commit()

    repo = TaskRepository(async_session)
    items, _ = await repo.list_paginated(
        page=1,
        page_size=10,
        sort_by="last_run_at",
        sort_dir="desc",
    )
    assert [t.name for t in items] == ["WithTime", "NoTime"]


@pytest.mark.asyncio
async def test_list_paginated_sort_last_run_at_asc_nulls_first(async_session) -> None:
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
    async_session.add_all(
        [
            Task(
                name="WithTime",
                start_url="https://t.example",
                cron_expr="* * * * *",
                status=1,
                last_run_at=base + timedelta(days=1),
            ),
            Task(
                name="NoTime",
                start_url="https://n.example",
                cron_expr="* * * * *",
                status=1,
                last_run_at=None,
            ),
        ]
    )
    await async_session.commit()

    repo = TaskRepository(async_session)
    items, _ = await repo.list_paginated(
        page=1,
        page_size=10,
        sort_by="last_run_at",
        sort_dir="asc",
    )
    assert [t.name for t in items] == ["NoTime", "WithTime"]
