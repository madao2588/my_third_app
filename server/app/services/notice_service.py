from pathlib import Path

from app.repositories.data_repo import DataRepository
from app.repositories.keyword_rule_repo import KeywordRepository
from app.schemas.common import PageData
from app.schemas.notice import NoticeListItem, NoticeRead, NoticeSnapshotRead
from app.utils.notice import (
    build_notice_summary,
    extract_matched_keywords,
    extract_source_site,
    is_high_priority_notice,
)


class NoticeService:
    def __init__(self, data_repo: DataRepository, keyword_repo: KeywordRepository):
        self.data_repo = data_repo
        self.keyword_repo = keyword_repo
        self.server_dir = Path(__file__).resolve().parents[2]

    async def _get_keyword_lists(self) -> tuple[list[str], list[str]]:
        rules = await self.keyword_repo.get_active()
        active = [r.word for r in rules if r.is_active]
        high_priority = [r.word for r in rules if r.is_high_priority and r.is_active]
        return active, high_priority

    async def list_notices(self, *, page: int, page_size: int, keyword: str | None = None) -> PageData[NoticeListItem]:
        items, total = await self.data_repo.list_paginated(
            page=page,
            page_size=page_size,
            keyword=keyword,
            enabled_only=True,
        )
        active_kws, high_pri_kws = await self._get_keyword_lists()
        notices = [self._to_notice_list_item(item, active_kws, high_pri_kws) for item in items]
        return PageData[NoticeListItem](
            items=notices,
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_notice(self, notice_id: int) -> NoticeRead:
        data = await self.data_repo.get_by_id(notice_id)
        if data is None:
            raise LookupError(f"Notice {notice_id} not found")

        active_kws, high_pri_kws = await self._get_keyword_lists()
        matched_keywords = extract_matched_keywords([data.title, data.content_text], active_kws)
        return NoticeRead(
            id=data.id,
            title=data.title or "",
            summary=build_notice_summary(data.content_text),
            source_site=extract_source_site(data.source_url),
            source_url=data.source_url,
            published_at=None,
            captured_at=data.fetch_time,
            quality_score=data.quality_score,
            matched_keywords=matched_keywords,
            is_high_priority=is_high_priority_notice(
                quality_score=data.quality_score,
                matched_keywords=matched_keywords,
                high_priority_keywords=high_pri_kws,
            ),
            task_id=data.task_id,
            content_text=data.content_text or "",
            content_html=data.content_html or "",
            content_hash=data.content_hash,
            snapshot_path=data.snapshot_path,
        )

    async def get_notice_snapshot(self, notice_id: int) -> NoticeSnapshotRead:
        data = await self.data_repo.get_by_id(notice_id)
        if data is None:
            raise LookupError(f"Notice {notice_id} not found")
        if not data.snapshot_path:
            raise FileNotFoundError(f"Snapshot for notice {notice_id} not found")

        snapshot_path = self.server_dir / data.snapshot_path
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot file {snapshot_path} not found")

        return NoticeSnapshotRead(
            id=data.id,
            source_url=data.source_url,
            source_site=extract_source_site(data.source_url),
            snapshot_path=data.snapshot_path,
            content=snapshot_path.read_text(encoding="utf-8"),
        )

    def _to_notice_list_item(self, item, active_keywords: list[str], high_priority_keywords: list[str]) -> NoticeListItem:
        matched_keywords = extract_matched_keywords([item.title, item.content_text], active_keywords)
        return NoticeListItem(
            id=item.id,
            title=item.title or "",
            summary=build_notice_summary(item.content_text),
            source_site=extract_source_site(item.source_url),
            source_url=item.source_url,
            published_at=None,
            captured_at=item.fetch_time,
            quality_score=item.quality_score,
            matched_keywords=matched_keywords,
            is_high_priority=is_high_priority_notice(
                quality_score=item.quality_score,
                matched_keywords=matched_keywords,
                high_priority_keywords=high_priority_keywords,
            ),
            task_id=item.task_id,
        )
