from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime, timedelta

from app.core.config import get_settings
from app.core.security import generate_session_token, hash_password, verify_password
from app.models.auth import User, UserSession
from app.repositories.auth_repo import AuthRepository
from app.schemas.auth import AuthSessionRead, LoginPayload, UserRead


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo
        self.settings = get_settings()

    async def ensure_default_admin(self) -> None:
        existing_user = await self.auth_repo.get_user_by_username(
            self.settings.default_admin_username,
        )
        if existing_user is not None:
            return

        password_hash, password_salt = hash_password(self.settings.default_admin_password)
        await self.auth_repo.create_user(
            username=self.settings.default_admin_username,
            password_hash=password_hash,
            password_salt=password_salt,
        )

    async def login(self, payload: LoginPayload) -> AuthSessionRead:
        user = await self.auth_repo.get_user_by_username(payload.username)
        if user is None:
            raise ValueError('用户名或密码不正确')

        if not verify_password(payload.password, user.password_salt, user.password_hash):
            raise ValueError('用户名或密码不正确')

        avatar_base64 = self._normalize_avatar(payload.avatar_base64)
        if avatar_base64 != user.avatar_base64:
            user = await self.auth_repo.update_user_avatar(user, avatar_base64)

        token = generate_session_token()
        expires_at = datetime.now(UTC) + timedelta(days=self.settings.session_ttl_days)
        session_obj = await self.auth_repo.create_session(user, token, expires_at)
        return self._build_session_response(user, session_obj)

    async def get_session(self, token: str) -> AuthSessionRead:
        session_obj = await self.auth_repo.get_session_by_token(token)
        if session_obj is None:
            raise PermissionError('登录已过期，请重新登录')

        if session_obj.expires_at.tzinfo is None:
            expires_at = session_obj.expires_at.replace(tzinfo=UTC)
        else:
            expires_at = session_obj.expires_at.astimezone(UTC)

        if expires_at <= datetime.now(UTC):
            await self.auth_repo.delete_session_by_token(token)
            raise PermissionError('登录已过期，请重新登录')

        await self.auth_repo.touch_session(session_obj)
        user = await self.auth_repo.get_user_by_id(session_obj.user_id)
        if user is None:
            await self.auth_repo.delete_session_by_token(token)
            raise PermissionError('登录已过期，请重新登录')

        return self._build_session_response(user, session_obj)

    async def logout(self, token: str) -> None:
        await self.auth_repo.delete_session_by_token(token)

    def _build_session_response(
        self,
        user: User,
        session_obj: UserSession,
    ) -> AuthSessionRead:
        return AuthSessionRead(
            access_token=session_obj.token,
            expires_at=session_obj.expires_at,
            user=UserRead(
                id=user.id,
                username=user.username,
                avatar_base64=user.avatar_base64,
            ),
        )

    def _normalize_avatar(self, avatar_base64: str | None) -> str | None:
        if avatar_base64 is None:
            return None

        trimmed = avatar_base64.strip()
        if not trimmed:
            return None

        # Validate that the avatar payload is valid base64 before storing it.
        try:
            base64.b64decode(trimmed, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError('头像文件格式无效') from exc
        return trimmed
