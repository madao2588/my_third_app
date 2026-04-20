from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class KeywordRuleBase(BaseModel):
    word: str = Field(..., min_length=1, max_length=100, description="The keyword itself")
    is_high_priority: bool = Field(False, description="Whether matches mark notices as high priority")
    is_active: bool = Field(True, description="Whether this rule is enabled")

class KeywordRuleCreate(KeywordRuleBase):
    pass

class KeywordRuleUpdate(BaseModel):
    word: str | None = Field(None, min_length=1, max_length=100)
    is_high_priority: bool | None = None
    is_active: bool | None = None

class KeywordRuleResponse(KeywordRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

class KeywordRuleListResponse(BaseModel):
    items: list[KeywordRuleResponse]
    total: int