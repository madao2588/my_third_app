from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import User, UserSession


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        username: str,
        password_hash: str,
        password_salt: str,
        avatar_base64: str | None = None,
    ) -> User:
        user = User(
            username=username,
            password_hash=password_hash,
            password_salt=password_salt,
            avatar_base64=avatar_base64,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user_avatar(self, user: User, avatar_base64: str | None) -> User:
        user.avatar_base64 = avatar_base64
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_session(
        self,
        user: User,
        token: str,
        expires_at: datetime,
    ) -> UserSession:
        session = UserSession(
            user_id=user.id,
            token=token,
            expires_at=expires_at,
            last_used_at=datetime.now(UTC),
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_session_by_token(self, token: str) -> UserSession | None:
        statement = select(UserSession).where(UserSession.token == token)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def touch_session(self, session_obj: UserSession) -> UserSession:
        session_obj.last_used_at = datetime.now(UTC)
        await self.session.commit()
        await self.session.refresh(session_obj)
        return session_obj

    async def delete_session_by_token(self, token: str) -> None:
        await self.session.execute(delete(UserSession).where(UserSession.token == token))
        await self.session.commit()
