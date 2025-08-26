"""Task API endpoints."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.models.task import TaskStatus
from app.schemas.task_schemas import (
    TaskCreate,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    description="Создает новую задачу с указанными параметрами.",
)
def create_task(task_data: TaskCreate) -> TaskResponse:
    """Create a new task."""
    task = task_service.create_task(task_data)
    return TaskResponse.model_validate(task)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу по ID",
    description="Возвращает задачу по указанному идентификатору.",
)
def get_task(task_id: UUID) -> TaskResponse:
    """Get task by ID."""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return TaskResponse.model_validate(task)


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Получить список задач",
    description="Возвращает список задач с возможностью фильтрации по статусу и пагинацией.",
)
def get_tasks(
    status: Optional[TaskStatus] = Query(
        None,
        description="Фильтр по статусу задачи"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Количество задач для пропуска"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Максимальное количество задач для возврата"
    ),
) -> TaskListResponse:
    """Get list of tasks with optional filtering and pagination."""
    tasks, total = task_service.get_tasks(status=status, skip=skip, limit=limit)
    
    task_responses = [TaskResponse.model_validate(task) for task in tasks]
    
    return TaskListResponse(
        tasks=task_responses,
        total=total,
        skip=skip,
        limit=limit
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу",
    description="Обновляет существующую задачу по указанному идентификатору.",
)
def update_task(task_id: UUID, task_data: TaskUpdate) -> TaskResponse:
    """Update an existing task."""
    updated_task = task_service.update_task(task_id, task_data)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу по указанному идентификатору.",
)
def delete_task(task_id: UUID) -> None:
    """Delete a task."""
    if not task_service.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {task_id} не найдена"
        )
