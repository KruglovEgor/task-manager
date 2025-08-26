"""Task service with business logic."""

from typing import List, Optional
from uuid import UUID

from app.database.storage import task_storage
from app.models.task import Task, TaskStatus
from app.schemas.task_schemas import TaskCreate, TaskUpdate


class TaskService:
    """Service for task operations."""
    
    def __init__(self) -> None:
        """Initialize service."""
        self.storage = task_storage
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task."""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status or TaskStatus.CREATED
        )
        return self.storage.create_task(task)
    
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID."""
        return self.storage.get_task(task_id)
    
    def get_tasks(
        self,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Task], int]:
        """Get list of tasks with optional filtering and pagination."""
        return self.storage.get_tasks(status=status, skip=skip, limit=limit)
    
    def update_task(self, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
        """Update an existing task."""
        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            return None
        
        # Create updated task with new data
        update_data = task_data.model_dump(exclude_unset=True)
        
        # Preserve original values for fields not being updated
        updated_task = existing_task.model_copy(deep=True)
        
        for field, value in update_data.items():
            setattr(updated_task, field, value)
        
        return self.storage.update_task(task_id, updated_task)
    
    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task."""
        return self.storage.delete_task(task_id)
    
    def task_exists(self, task_id: UUID) -> bool:
        """Check if task exists."""
        return self.storage.get_task(task_id) is not None


# Global service instance
task_service = TaskService()
