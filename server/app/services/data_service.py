import csv
import io
import json
import re
from pathlib import Path

from app.repositories.data_repo import DataRepository
from app.repositories.log_repo import LogRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.common import (
    LogRead,
    LogSummary,
    PageData,
    RunSummaryPayload,
    StatsOverview,
)
from app.schemas.data import DataListItem, DataRead, SnapshotRead


_RUN_ID_RE = re.compile(r"\[run=(?P<run_id>[0-9a-zA-Z_-]+)\]")
_SUMMARY_RE = re.compile(r"(?P<mode>list_follow|single_page)\s+summary:\s*(?P<body>.+)$")


def _parse_metrics_text(body: str) -> dict[str, str | int | bool]:
    metrics: dict[str, str | int | bool] = {}
    for chunk in body.split(","):
        part = chunk.strip()
        if "=" not in part:
            continue
        key, raw_value = part.split("=", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key or not value:
            continue

        lowered = value.lower()
        if lowered in {"true", "false"}:
            metrics[key] = lowered == "true"
            continue
        try:
            metrics[key] = int(value)
            continue
        except ValueError:
            metrics[key] = value
    return metrics


def parse_run_summary_from_log(
    *,
    message: str,
    run_summary: str | None,
    error_stack: str | None,
) -> RunSummaryPayload | None:
    text = (message or "").strip()
    if run_summary:
        try:
            raw = json.loads(run_summary)
            if (
                isinstance(raw, dict)
                and raw.get("kind") == "run_summary"
                and isinstance(raw.get("mode"), str)
                and isinstance(raw.get("metrics"), dict)
            ):
                metrics_dict = {
                    str(k): v
                    for k, v in raw["metrics"].items()
                    if isinstance(v, (str, int, bool))
                }
                return RunSummaryPayload(
                    run_id=raw.get("run_id")
                    if isinstance(raw.get("run_id"), str)
                    else None,
                    mode=raw["mode"],
                    metrics=metrics_dict,
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    # Backward compatibility for older rows where structured summary lived in error_stack.
    if error_stack:
        try:
            raw = json.loads(error_stack)
            if (
                isinstance(raw, dict)
                and raw.get("kind") == "run_summary"
                and isinstance(raw.get("mode"), str)
                and isinstance(raw.get("metrics"), dict)
            ):
                metrics_dict = {
                    str(k): v
                    for k, v in raw["metrics"].items()
                    if isinstance(v, (str, int, bool))
                }
                return RunSummaryPayload(
                    run_id=raw.get("run_id")
                    if isinstance(raw.get("run_id"), str)
                    else None,
                    mode=raw["mode"],
                    metrics=metrics_dict,
                )
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    if not text:
        return None
    summary_match = _SUMMARY_RE.search(text)
    if summary_match is None:
        return None

    metrics = _parse_metrics_text(summary_match.group("body"))
    run_match = _RUN_ID_RE.search(text)
    run_id = run_match.group("run_id") if run_match else None

    return RunSummaryPayload(
        run_id=run_id,
        mode=summary_match.group("mode"),
        metrics=metrics,
    )


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
        message_contains: str | None = None,
        only_summary: bool = False,
    ) -> PageData[LogRead]:
        needle = (message_contains or "").strip()
        if len(needle) > 500:
            needle = needle[:500]

        items, total = await self.log_repo.list_paginated(
            page=page,
            page_size=page_size,
            task_id=task_id,
            level=level,
            message_contains=needle or None,
            only_summary=only_summary,
        )
        logs = [
            LogRead(
                id=item.id,
                task_id=item.task_id,
                level=item.level,
                message=item.message,
                error_stack=item.error_stack,
                run_summary=parse_run_summary_from_log(
                    message=item.message,
                    run_summary=item.run_summary,
                    error_stack=item.error_stack,
                ),
                created_at=item.created_at,
            )
            for item in items
        ]
        return PageData[LogRead](
            items=logs,
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

    async def export_collected_data_csv(
        self,
        *,
        task_id: int | None,
        limit: int,
    ) -> bytes:
        rows = await self.data_repo.list_recent_for_export(task_id=task_id, limit=limit)
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(
            [
                "id",
                "task_id",
                "title",
                "source_url",
                "quality_score",
                "fetch_time",
                "content_hash",
                "snapshot_path",
                "content_preview",
            ],
        )
        for row in rows:
            preview = (row.content_text or "")[:4000].replace("\r\n", "\n").replace("\r", "\n")
            ft = row.fetch_time.isoformat() if row.fetch_time else ""
            writer.writerow(
                [
                    row.id,
                    row.task_id,
                    row.title or "",
                    row.source_url,
                    row.quality_score,
                    ft,
                    row.content_hash or "",
                    row.snapshot_path or "",
                    preview,
                ],
            )
        return ("\ufeff" + buffer.getvalue()).encode("utf-8")
