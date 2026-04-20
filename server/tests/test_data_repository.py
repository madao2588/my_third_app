import pytest
from sqlalchemy import select

from app.models.data import CollectedData
from app.models.task import Task
from app.repositories.data_repo import DataRepository
from app.schemas.task import TaskStatus


@pytest.mark.asyncio
async def test_list_recent_for_export_all_tasks(async_session) -> None:
    async_session.add(
        Task(
            name="T1",
            start_url="https://a.example",
            cron_expr="* * * * *",
            status=int(TaskStatus.ENABLED),
        )
    )
    await async_session.flush()
    tid = (await async_session.execute(select(Task.id))).scalar_one()
    async_session.add_all(
        [
            CollectedData(
                task_id=tid,
                title="Old",
                content_html=None,
                content_text="a",
                source_url="https://a.example/1",
                snapshot_path=None,
                quality_score=0,
                content_hash=None,
            ),
            CollectedData(
                task_id=tid,
                title="New",
                content_html=None,
                content_text="b",
                source_url="https://a.example/2",
                snapshot_path=None,
                quality_score=0,
                content_hash=None,
            ),
        ]
    )
    await async_session.commit()

    repo = DataRepository(async_session)
    rows = await repo.list_recent_for_export(task_id=None, limit=10)
    assert len(rows) == 2
    assert rows[0].title == "New"
    assert rows[1].title == "Old"


@pytest.mark.asyncio
async def test_list_recent_for_export_filters_task_id(async_session) -> None:
    async_session.add_all(
        [
            Task(
                name="A",
                start_url="https://a.example",
                cron_expr="* * * * *",
                status=1,
            ),
            Task(
                name="B",
                start_url="https://b.example",
                cron_expr="* * * * *",
                status=1,
            ),
        ]
    )
    await async_session.flush()
    ids = (await async_session.execute(select(Task.id).order_by(Task.id))).scalars().all()
    id_a, id_b = ids[0], ids[1]
    async_session.add_all(
        [
            CollectedData(
                task_id=id_a,
                title=None,
                content_html=None,
                content_text="x",
                source_url="https://x/1",
                snapshot_path=None,
                quality_score=0,
                content_hash=None,
            ),
            CollectedData(
                task_id=id_b,
                title=None,
                content_html=None,
                content_text="y",
                source_url="https://y/1",
                snapshot_path=None,
                quality_score=0,
                content_hash=None,
            ),
        ]
    )
    await async_session.commit()

    repo = DataRepository(async_session)
    rows = await repo.list_recent_for_export(task_id=id_a, limit=10)
    assert len(rows) == 1
    assert rows[0].task_id == id_a


@pytest.mark.asyncio
async def test_list_paginated_no_filters(async_session) -> None:
    async_session.add(
        Task(
            name="T",
            start_url="https://t.example",
            cron_expr="* * * * *",
            status=1,
        )
    )
    await async_session.flush()
    tid = (await async_session.execute(select(Task.id))).scalar_one()
    async_session.add(
        CollectedData(
            task_id=tid,
            title="Row",
            content_html=None,
            content_text="body",
            source_url="https://t.example/p",
            snapshot_path=None,
            quality_score=1,
            content_hash="h1",
        )
    )
    await async_session.commit()

    repo = DataRepository(async_session)
    items, total = await repo.list_paginated(page=1, page_size=20)
    assert total == 1
    assert len(items) == 1
    assert items[0].source_url == "https://t.example/p"
