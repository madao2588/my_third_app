from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.notice import NoticeListItem


class KeywordHeatItem(BaseModel):
    keyword: str
    count: int = Field(..., ge=0)


class SourceDistributionItem(BaseModel):
    source_site: str
    notice_count: int = Field(..., ge=0)
    percentage: float = Field(..., ge=0, le=100)


class DashboardMetrics(BaseModel):
    today_new_notices: int = Field(..., ge=0)
    keyword_hit_notices: int = Field(..., ge=0)
    monitoring_site_count: int = Field(..., ge=0)
    high_priority_notices: int = Field(..., ge=0)


class DashboardOverview(BaseModel):
    metrics: DashboardMetrics
    high_value_notices: list[NoticeListItem]
    recent_notices: list[NoticeListItem]
    keyword_heat: list[KeywordHeatItem]
    source_distribution: list[SourceDistributionItem]
    last_updated_at: datetime | None = None
