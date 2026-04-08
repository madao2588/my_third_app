from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_data_service
from app.schemas.common import ApiResponse, PageData
from app.schemas.data import DataListItem, DataRead, SnapshotRead
from app.services.data_service import DataService

router = APIRouter(prefix="/data", tags=["data"])


@router.get("", response_model=ApiResponse[PageData[DataListItem]])
async def list_data(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    task_id: int | None = Query(default=None),
    service: DataService = Depends(get_data_service),
) -> ApiResponse[PageData[DataListItem]]:
    data = await service.list_data(page=page, page_size=page_size, task_id=task_id)
    return ApiResponse(data=data)


@router.get("/{data_id}", response_model=ApiResponse[DataRead])
async def get_data(
    data_id: int,
    service: DataService = Depends(get_data_service),
) -> ApiResponse[DataRead]:
    try:
        data = await service.get_data(data_id)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{data_id}/snapshot", response_model=ApiResponse[SnapshotRead])
async def get_snapshot(
    data_id: int,
    service: DataService = Depends(get_data_service),
) -> ApiResponse[SnapshotRead]:
    try:
        data = await service.get_snapshot_content(data_id)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
