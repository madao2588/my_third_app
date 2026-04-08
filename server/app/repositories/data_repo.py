from collections.abc import Sequence
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.data import CollectedData


class DataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        task_id: int,
        title: str | None,
        content_html: str | None,
        content_text: str | None,
        source_url: str,
        snapshot_path: str | None,
        quality_score: int,
        content_hash: str | None,
    ) -> CollectedData:
        data = CollectedData(
            task_id=task_id,
            title=title,
            content_html=content_html,
            content_text=content_text,
            source_url=source_url,
            snapshot_path=snapshot_path,
            quality_score=quality_score,
            content_hash=content_hash,
        )
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_by_source_url(self, source_url: str) -> CollectedData | None:
        statement = select(CollectedData).where(CollectedData.source_url == source_url).order_by(CollectedData.id.desc())
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def update(self, data: CollectedData, **kwargs) -> CollectedData:
        for k, v in kwargs.items():
            setattr(data, k, v)
        from datetime import datetime, timezone
        data.fetch_time = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_by_id(self, data_id: int) -> CollectedData | None:
        statement = select(CollectedData).where(CollectedData.id == data_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_hash(self, content_hash: str) -> CollectedData | None:
        statement = select(CollectedData).where(CollectedData.content_hash == content_hash)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_paginated(
        self,
        *,
        page: int,
        page_size: int,
        task_id: int | None = None,
        keyword: str | None = None,
    ) -> tuple[Sequence[CollectedData], int]:
        from sqlalchemy import or_
        filters = []
        if task_id is not None:
            filters.append(CollectedData.task_id == task_id)
        if keyword:
            filters.append(
                or_(
                    CollectedData.title.ilike(f'%{keyword}%'),
                    CollectedData.content_text.ilike(f'%{keyword}%')
                )
            )

        total_statement = select(func.count()).select_from(CollectedData)
        if filters:
            total_statement = total_statement.where(*filters)
        total = await self.session.scalar(total_statement) or 0

        statement = (
            select(CollectedData)
            .where(*filters)
            .order_by(CollectedData.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.execute(statement)
        return result.scalars().all(), total

    async def update_snapshot_path(
        self,
        *,
        data: CollectedData,
        snapshot_path: str,
    ) -> CollectedData:
        data.snapshot_path = snapshot_path
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def count_all(self) -> int:
        statement = select(func.count()).select_from(CollectedData)
        return await self.session.scalar(statement) or 0

    async def count_today(self) -> int:
        today = date.today().isoformat()
        statement = select(func.count()).select_from(CollectedData).where(
            func.date(CollectedData.fetch_time) == today
        )
        return await self.session.scalar(statement) or 0

    async def average_quality_score(self) -> float:
        statement = select(func.avg(CollectedData.quality_score))
        average = await self.session.scalar(statement)
        return float(average or 0.0)
