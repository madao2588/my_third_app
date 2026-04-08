from datetime import datetime

from pydantic import BaseModel, Field


class DataRead(BaseModel):
    id: int
    task_id: int
    title: str | None = None
    content_html: str | None = None
    content_text: str | None = None
    source_url: str = Field(..., min_length=1, max_length=2048)
    snapshot_path: str | None = None
    quality_score: int = Field(..., ge=0, le=100)
    content_hash: str | None = None
    fetch_time: datetime

    model_config = {"from_attributes": True}


class DataListItem(DataRead):
    pass


class SnapshotRead(BaseModel):
    id: int
    snapshot_path: str
    content: str
