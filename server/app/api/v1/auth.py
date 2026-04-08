from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.dependencies import get_auth_service
from app.schemas.auth import AuthSessionRead, LoginPayload
from app.schemas.common import ApiResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


async def _get_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authorization header missing',
        )

    scheme, _, token = authorization.partition(' ')
    if scheme.lower() != 'bearer' or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token format',
        )

    return token.strip()


@router.post('/login', response_model=ApiResponse[AuthSessionRead])
async def login(
    payload: LoginPayload,
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[AuthSessionRead]:
    try:
        session_data = await service.login(payload)
        return ApiResponse(data=session_data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get('/me', response_model=ApiResponse[AuthSessionRead])
async def me(
    authorization: str | None = Header(default=None),
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[AuthSessionRead]:
    token = await _get_bearer_token(authorization)
    try:
        session_data = await service.get_session(token)
        return ApiResponse(data=session_data)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post('/logout', response_model=ApiResponse[dict[str, str]])
async def logout(
    authorization: str | None = Header(default=None),
    service: AuthService = Depends(get_auth_service),
) -> ApiResponse[dict[str, str]]:
    token = await _get_bearer_token(authorization)
    await service.logout(token)
    return ApiResponse(data={'message': 'success'})
