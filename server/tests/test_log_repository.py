import pytest

from app.models.log import LogEntry
from app.repositories.log_repo import LogRepository


@pytest.mark.asyncio
async def test_list_paginated_no_filters(async_session) -> None:
    async_session.add(LogEntry(level="INFO", message="a", task_id=None))
    async_session.add(LogEntry(level="WARN", message="b", task_id=None))
    await async_session.commit()

    repo = LogRepository(async_session)
    items, total = await repo.list_paginated(page=1, page_size=10)
    assert total == 2
    assert len(items) == 2


@pytest.mark.asyncio
async def test_list_paginated_message_contains(async_session) -> None:
    async_session.add(LogEntry(level="INFO", message="hello world", task_id=None))
    async_session.add(LogEntry(level="INFO", message="other", task_id=None))
    async_session.add(
        LogEntry(
            level="ERROR",
            message="x",
            task_id=None,
            error_stack="trace contains NEEDLE here",
        )
    )
    await async_session.commit()

    repo = LogRepository(async_session)
    items, total = await repo.list_paginated(
        page=1,
        page_size=10,
        message_contains="NEEDLE",
    )
    assert total == 1
    assert "NEEDLE" in (items[0].error_stack or "")


@pytest.mark.asyncio
async def test_list_paginated_only_summary(async_session) -> None:
    async_session.add(
        LogEntry(
            level="INFO",
            message="normal log",
            task_id=None,
        )
    )
    async_session.add(
        LogEntry(
            level="INFO",
            message="[run=a] 单页运行摘要：处理 1，入库 1，重复跳过 0，失败 0。",
            task_id=None,
            run_summary='{"kind":"run_summary","run_id":"a","mode":"single_page","metrics":{"processed":1}}',
        )
    )
    async_session.add(
        LogEntry(
            level="INFO",
            message="[run=b] single_page summary: processed=1, stored=1",
            task_id=None,
            error_stack='{"kind":"run_summary","run_id":"b","mode":"single_page","metrics":{"processed":1}}',
        )
    )
    await async_session.commit()

    repo = LogRepository(async_session)
    items, total = await repo.list_paginated(
        page=1,
        page_size=10,
        only_summary=True,
    )
    assert total == 2
    assert len(items) == 2
