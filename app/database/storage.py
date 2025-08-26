from typing import List, Optional
from uuid import UUID

from app.database.connection import get_db
from app.database.models import TaskModel, TaskStatusEnum
from app.models.task import Task, TaskStatus


class TaskStorage:
    def __init__(self) -> None:
        pass
    
    def _convert_to_model(self, task: Task) -> TaskModel:
        return TaskModel(
            id=str(task.id),
            title=task.title,
            description=task.description,
            status=TaskStatusEnum(task.status),
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    def _convert_from_model(self, task_model: TaskModel) -> Task:
        return Task(
            id=UUID(task_model.id),
            title=task_model.title,
            description=task_model.description,
            status=TaskStatus(task_model.status),
            created_at=task_model.created_at,
            updated_at=task_model.updated_at
        )
    
    def create_task(self, task: Task) -> Task:
        db = next(get_db())
        try:
            task_model = self._convert_to_model(task)
            db.add(task_model)
            db.commit()
            db.refresh(task_model)
            return self._convert_from_model(task_model)
        finally:
            db.close()
    
    def get_task(self, task_id: UUID) -> Optional[Task]:
        db = next(get_db())
        try:
            task_model = db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            if task_model:
                return self._convert_from_model(task_model)
            return None
        finally:
            db.close()
    
    def get_tasks(
        self,
        status: Optional[TaskStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[Task], int]:
        db = next(get_db())
        try:
            query = db.query(TaskModel)
            
            if status:
                query = query.filter(TaskModel.status == TaskStatusEnum(status))
            
            total = query.count()
            tasks = query.order_by(TaskModel.created_at.desc()).offset(skip).limit(limit).all()
            
            return [self._convert_from_model(task) for task in tasks], total
        finally:
            db.close()
    
    def update_task(self, task_id: UUID, updated_task: Task) -> Optional[Task]:
        db = next(get_db())
        try:
            task_model = db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            if not task_model:
                return None
            
            task_model.title = updated_task.title
            task_model.description = updated_task.description
            task_model.status = TaskStatusEnum(updated_task.status)
            
            db.commit()
            db.refresh(task_model)
            return self._convert_from_model(task_model)
        finally:
            db.close()
    
    def delete_task(self, task_id: UUID) -> bool:
        db = next(get_db())
        try:
            task_model = db.query(TaskModel).filter(TaskModel.id == str(task_id)).first()
            if not task_model:
                return False
            
            db.delete(task_model)
            db.commit()
            return True
        finally:
            db.close()
    
    def count(self) -> int:
        db = next(get_db())
        try:
            return db.query(TaskModel).count()
        finally:
            db.close()


task_storage = TaskStorage()
