from collections.abc import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.keyword_rule import KeywordRule
from app.schemas.keyword_rule import KeywordRuleCreate, KeywordRuleUpdate

class KeywordRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def all(self) -> Sequence[KeywordRule]:
        result = await self._session.execute(select(KeywordRule).order_by(KeywordRule.id.desc()))
        return result.scalars().all()

    async def get_active(self) -> list[KeywordRule]:
        result = await self._session.execute(
            select(KeywordRule).where(KeywordRule.is_active == True)
        )
        return list(result.scalars().all())

    async def get_by_id(self, rule_id: int) -> Optional[KeywordRule]:
        return await self._session.get(KeywordRule, rule_id)

    async def get_by_word(self, word: str) -> Optional[KeywordRule]:
        result = await self._session.execute(
            select(KeywordRule).where(KeywordRule.word == word)
        )
        return result.scalars().first()

    async def create(self, kw_schema: KeywordRuleCreate) -> KeywordRule:
        rule = KeywordRule(
            word=kw_schema.word,
            is_high_priority=kw_schema.is_high_priority,
            is_active=kw_schema.is_active
        )
        self._session.add(rule)
        await self._session.commit()
        await self._session.refresh(rule)
        return rule

    async def update(self, rule: KeywordRule, updates: KeywordRuleUpdate) -> KeywordRule:
        update_data = updates.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(rule, key, value)
        await self._session.commit()
        await self._session.refresh(rule)
        return rule

    async def delete(self, rule: KeywordRule) -> None:
        await self._session.delete(rule)
        await self._session.commit()