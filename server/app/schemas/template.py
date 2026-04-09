from datetime import datetime

from pydantic import BaseModel, Field


class TaskTemplateBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    start_url: str = Field(..., min_length=1, max_length=2048)
    cron_expr: str = Field(..., min_length=1, max_length=100)
    parser_rules: str | None = None
    enabled: bool = True
    description: str = Field(..., min_length=1, max_length=500)
    tags: list[str] = Field(default_factory=list)


class TaskTemplateCreate(TaskTemplateBase):
    id: str | None = Field(default=None, min_length=1)


class TaskTemplateUpdate(TaskTemplateBase):
    pass


class TaskTemplateRead(TaskTemplateBase):
    id: str = Field(..., min_length=1)
    usage_count: int = Field(default=0, ge=0)
    last_used_at: datetime | None = None


class TestTemplateRequest(BaseModel):
    start_url: str = Field(..., min_length=1, max_length=2048)
    parser_rules: str | None = None


class TestTemplateResponse(BaseModel):
    title: str | None = None
    content_text: str | None = None
    content_html: str | None = None
    quality_score: int | None = None
    error: str | None = None

