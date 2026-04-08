from collections import Counter

from app.repositories.data_repo import DataRepository
from app.repositories.keyword_rule_repo import KeywordRepository
from app.repositories.task_repo import TaskRepository
from app.schemas.dashboard import (
    DashboardMetrics,
    DashboardOverview,
    KeywordHeatItem,
    SourceDistributionItem,
)
from app.services.notice_service import NoticeService
from app.utils.notice import (
    keyword_heat_from_texts,
)


class DashboardService:
    def __init__(self, data_repo: DataRepository, task_repo: TaskRepository, keyword_repo: KeywordRepository):
        self.data_repo = data_repo
        self.task_repo = task_repo
        self.keyword_repo = keyword_repo
        self.notice_service = NoticeService(data_repo=data_repo, keyword_repo=keyword_repo)

    async def get_overview(self) -> DashboardOverview:
        recent_items, _ = await self.data_repo.list_paginated(page=1, page_size=20)
        all_items, _ = await self.data_repo.list_paginated(page=1, page_size=500)
        enabled_tasks = await self.task_repo.list_enabled()

        active_kws, high_pri_kws = await self.notice_service._get_keyword_lists()

        notice_items = [self.notice_service._to_notice_list_item(item, active_kws, high_pri_kws) for item in all_items]
        recent_notices = [self.notice_service._to_notice_list_item(item, active_kws, high_pri_kws) for item in recent_items[:5]]
        high_value_notices = sorted(
            notice_items,
            key=lambda item: (item.is_high_priority, item.quality_score, item.captured_at),
            reverse=True,
        )[:5]

        keyword_hit_notices = sum(1 for item in notice_items if item.matched_keywords)
        high_priority_notices = sum(1 for item in notice_items if item.is_high_priority)
        source_distribution = self._build_source_distribution(notice_items)
        keyword_heat = self._build_keyword_heat(notice_items, active_kws)
        last_updated_at = max((item.captured_at for item in notice_items), default=None)

        return DashboardOverview(
            metrics=DashboardMetrics(
                today_new_notices=await self.data_repo.count_today(),
                keyword_hit_notices=keyword_hit_notices,
                monitoring_site_count=max(len(enabled_tasks), len(source_distribution)),
                high_priority_notices=high_priority_notices,
            ),
            high_value_notices=high_value_notices,
            recent_notices=recent_notices,
            keyword_heat=keyword_heat,
            source_distribution=source_distribution,
            last_updated_at=last_updated_at,
        )

    def _build_keyword_heat(self, notice_items, active_keywords: list[str]) -> list[KeywordHeatItem]:
        texts = [
            " ".join(
                filter(
                    None,
                    [
                        item.title,
                        item.summary,
                        " ".join(item.matched_keywords),
                    ],
                )
            )
            for item in notice_items
        ]
        return [
            KeywordHeatItem(keyword=keyword, count=count)
            for keyword, count in keyword_heat_from_texts(texts, active_keywords)
        ]

    def _build_source_distribution(self, notice_items) -> list[SourceDistributionItem]:
        total = len(notice_items)
        if total == 0:
            return []

        counter: Counter[str] = Counter(item.source_site for item in notice_items)
        return [
            SourceDistributionItem(
                source_site=source_site,
                notice_count=count,
                percentage=round((count / total) * 100, 2),
            )
            for source_site, count in counter.most_common(10)
        ]
