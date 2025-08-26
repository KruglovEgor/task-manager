"""Task schemas for API requests and responses."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(default=TaskStatus.CREATED, description="Task status")
    
    class Config:
        """Pydantic configuration."""
        
        schema_extra = {
            "example": {
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    
    class Config:
        """Pydantic configuration."""
        
        schema_extra = {
            "example": {
                "title": "Изучить FastAPI (обновлено)",
                "description": "Прочитать документацию, создать тестовое приложение и написать тесты",
                "status": "в работе"
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response."""
    
    id: UUID = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str,
        }
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано",
                "created_at": "2023-12-01T10:00:00",
                "updated_at": "2023-12-01T10:00:00"
            }
        }


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Number of items to return")


class TaskListResponse(BaseModel):
    """Schema for task list response with pagination."""
    
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items returned")
    
    class Config:
        """Pydantic configuration."""
        
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "title": "Изучить FastAPI",
                        "description": "Прочитать документацию и создать тестовое приложение",
                        "status": "создано",
                        "created_at": "2023-12-01T10:00:00",
                        "updated_at": "2023-12-01T10:00:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 10
            }
        }
