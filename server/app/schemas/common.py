from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T | None = None


class HealthPayload(BaseModel):
    status: str
    app_name: str


class EmptyPayload(BaseModel):
    pass


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PageData(BaseModel, Generic[T]):
    items: list[T]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)


class LogRead(BaseModel):
    id: int
    task_id: int | None = None
    level: str
    message: str
    error_stack: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LogSummary(BaseModel):
    total_logs: int = Field(..., ge=0)
    info_logs: int = Field(..., ge=0)
    warning_logs: int = Field(..., ge=0)
    error_logs: int = Field(..., ge=0)
    failed_task_count: int = Field(..., ge=0)


class StatsOverview(BaseModel):
    total_tasks: int = Field(..., ge=0)
    enabled_tasks: int = Field(..., ge=0)
    total_data: int = Field(..., ge=0)
    today_data: int = Field(..., ge=0)
    total_logs: int = Field(..., ge=0)
    avg_quality_score: float = Field(..., ge=0, le=100)
