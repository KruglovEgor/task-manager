"""Task model definition."""

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task status enumeration."""
    
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class Task(BaseModel):
    """Task model."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique task identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.CREATED, description="Task status")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Creation timestamp")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Last update timestamp")
    
    class Config:
        """Pydantic configuration."""
        
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: str,
        }
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Изучить FastAPI",
                "description": "Прочитать документацию и создать тестовое приложение",
                "status": "создано",
                "created_at": "2023-12-01T10:00:00",
                "updated_at": "2023-12-01T10:00:00"
            }
        }
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)
