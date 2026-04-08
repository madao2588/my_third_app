from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_task_service
from app.schemas.common import ApiResponse, EmptyPayload, PageData
from app.schemas.task import TaskCreate, TaskRead, TaskRunPayload, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=ApiResponse[PageData[TaskRead]])
async def list_tasks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[PageData[TaskRead]]:
    data = await service.list_tasks(page=page, page_size=page_size)
    return ApiResponse(data=data)


@router.get("/{task_id}", response_model=ApiResponse[TaskRead])
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskRead]:
    try:
        data = await service.get_task(task_id)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("", response_model=ApiResponse[TaskRead])
async def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskRead]:
    try:
        data = await service.create_task(payload)
        return ApiResponse(data=data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/{task_id}", response_model=ApiResponse[TaskRead])
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskRead]:
    try:
        data = await service.update_task(task_id, payload)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{task_id}", response_model=ApiResponse[EmptyPayload])
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[EmptyPayload]:
    try:
        data = await service.delete_task(task_id)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{task_id}/run", response_model=ApiResponse[TaskRunPayload])
async def run_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> ApiResponse[TaskRunPayload]:
    try:
        data = await service.run_task_now(task_id)
        return ApiResponse(data=data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
