from pathlib import Path

from app.repositories.data_repo import DataRepository
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.common import LogRead, LogSummary, PageData, StatsOverview
from app.schemas.data import DataListItem, DataRead, SnapshotRead


class DataService:
    def __init__(
        self,
        data_repo: DataRepository,
        task_repo: TaskRepository,
        log_repo: LogRepository,
    ):
        self.data_repo = data_repo
        self.task_repo = task_repo
        self.log_repo = log_repo
        self.server_dir = Path(__file__).resolve().parents[2]

    async def list_data(
        self,
        *,
        page: int,
        page_size: int,
        task_id: int | None = None,
    ) -> PageData[DataListItem]:
        items, total = await self.data_repo.list_paginated(
            page=page,
            page_size=page_size,
            task_id=task_id,
        )
        return PageData[DataListItem](
            items=[DataListItem.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_data(self, data_id: int) -> DataRead:
        data = await self.data_repo.get_by_id(data_id)
        if data is None:
            raise LookupError(f"Collected data {data_id} not found")
        return DataRead.model_validate(data)

    async def get_snapshot_content(self, data_id: int) -> SnapshotRead:
        data = await self.data_repo.get_by_id(data_id)
        if data is None:
            raise LookupError(f"Collected data {data_id} not found")
        if not data.snapshot_path:
            raise FileNotFoundError(f"Snapshot for data {data_id} not found")

        snapshot_path = self.server_dir / data.snapshot_path
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot file {snapshot_path} not found")
        return SnapshotRead(
            id=data.id,
            snapshot_path=data.snapshot_path,
            content=snapshot_path.read_text(encoding="utf-8"),
        )

    async def list_logs(
        self,
        *,
        page: int,
        page_size: int,
        task_id: int | None = None,
        level: str | None = None,
    ) -> PageData[LogRead]:
        items, total = await self.log_repo.list_paginated(
            page=page,
            page_size=page_size,
            task_id=task_id,
            level=level,
        )
        return PageData[LogRead](
            items=[LogRead.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_overview_stats(self) -> StatsOverview:
        total_tasks = await self.task_repo.count_all()
        enabled_tasks = await self.task_repo.count_enabled()
        total_data = await self.data_repo.count_all()
        today_data = await self.data_repo.count_today()
        total_logs = await self.log_repo.count_all()
        avg_quality_score = await self.data_repo.average_quality_score()

        return StatsOverview(
            total_tasks=total_tasks,
            enabled_tasks=enabled_tasks,
            total_data=total_data,
            today_data=today_data,
            total_logs=total_logs,
            avg_quality_score=avg_quality_score,
        )

    async def get_log_summary(self) -> LogSummary:
        total_logs = await self.log_repo.count_all()
        info_logs = await self.log_repo.count_by_level("INFO")
        warning_logs = await self.log_repo.count_by_level("WARNING")
        error_logs = await self.log_repo.count_by_level("ERROR")
        failed_task_count = await self.log_repo.count_failed_tasks()

        return LogSummary(
            total_logs=total_logs,
            info_logs=info_logs,
            warning_logs=warning_logs,
            error_logs=error_logs,
            failed_task_count=failed_task_count,
        )
