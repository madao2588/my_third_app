from enum import IntEnum
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TaskStatus(IntEnum):
    DISABLED = 0
    ENABLED = 1


class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    start_url: str = Field(..., min_length=1, max_length=2048)
    parser_rules: str | None = None
    cron_expr: str = Field(..., min_length=1, max_length=100)
    status: TaskStatus = TaskStatus.ENABLED

    @field_validator("start_url")
    @classmethod
    def validate_start_url(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("start_url must start with http:// or https://")
        return value


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    start_url: str | None = Field(default=None, min_length=1, max_length=2048)
    parser_rules: str | None = None
    cron_expr: str | None = Field(default=None, min_length=1, max_length=100)
    status: TaskStatus | None = None

    @field_validator("start_url")
    @classmethod
    def validate_start_url(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith(("http://", "https://")):
            raise ValueError("start_url must start with http:// or https://")
        return value


class TaskRead(TaskBase):
    id: int
    last_run_status: str | None = None
    last_run_at: datetime | None = None
    last_success_at: datetime | None = None
    last_error_message: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskRunPayload(BaseModel):
    task_id: int
    status: str
