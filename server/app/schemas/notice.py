from datetime import datetime

from pydantic import BaseModel, Field


class NoticeListItem(BaseModel):
    id: int
    title: str = ""
    summary: str = ""
    source_site: str
    source_url: str = Field(..., min_length=1, max_length=2048)
    published_at: datetime | None = None
    captured_at: datetime
    quality_score: int = Field(..., ge=0, le=100)
    matched_keywords: list[str] = []
    is_high_priority: bool = False
    task_id: int


class NoticeRead(NoticeListItem):
    content_text: str = ""
    content_html: str = ""
    content_hash: str | None = None
    snapshot_path: str | None = None


class NoticeSnapshotRead(BaseModel):
    id: int
    source_url: str
    source_site: str
    snapshot_path: str
    content: str
