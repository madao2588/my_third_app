from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LoginPayload(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=255)
    avatar_base64: str | None = None


class UserRead(BaseModel):
    id: int
    username: str
    avatar_base64: str | None = None

    model_config = {"from_attributes": True}


class AuthSessionRead(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    expires_at: datetime
    user: UserRead
