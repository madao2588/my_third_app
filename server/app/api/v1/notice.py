from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_notice_service
from app.schemas.common import ApiResponse, PageData
from app.schemas.notice import NoticeListItem, NoticeRead, NoticeSnapshotRead
from app.services.notice_service import NoticeService

router = APIRouter(prefix="/notices", tags=["notices"])


@router.get("", response_model=ApiResponse[PageData[NoticeListItem]])
async def list_notices(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    keyword: str | None = Query(default=None),
    service: NoticeService = Depends(get_notice_service),
) -> ApiResponse[PageData[NoticeListItem]]:
    return ApiResponse(data=await service.list_notices(page=page, page_size=page_size, keyword=keyword))


@router.get("/{notice_id}", response_model=ApiResponse[NoticeRead])
async def get_notice(
    notice_id: int,
    service: NoticeService = Depends(get_notice_service),
) -> ApiResponse[NoticeRead]:
    try:
        return ApiResponse(data=await service.get_notice(notice_id))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{notice_id}/snapshot", response_model=ApiResponse[NoticeSnapshotRead])
async def get_notice_snapshot(
    notice_id: int,
    service: NoticeService = Depends(get_notice_service),
) -> ApiResponse[NoticeSnapshotRead]:
    try:
        return ApiResponse(data=await service.get_notice_snapshot(notice_id))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
