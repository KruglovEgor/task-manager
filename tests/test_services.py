"""Service layer tests."""

import pytest
from uuid import uuid4

from app.models.task import Task, TaskStatus
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.services.task_service import TaskService


class TestTaskService:
    """Test cases for TaskService."""

    @pytest.fixture
    def task_service(self):
        """Create a task service instance."""
        return TaskService()

    def test_create_task(self, task_service):
        """Test task creation."""
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        
        task = task_service.create_task(task_data)
        
        assert task.title == task_data.title
        assert task.description == task_data.description
        assert task.status == task_data.status
        assert task.id is not None

    def test_create_task_with_default_status(self, task_service):
        """Test task creation with default status."""
        task_data = TaskCreate(
            title="Test Task",
            description="Test description"
        )
        
        task = task_service.create_task(task_data)
        
        assert task.status == TaskStatus.CREATED

    def test_get_task(self, task_service):
        """Test getting a task by ID."""
        # First create a task
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        created_task = task_service.create_task(task_data)
        
        # Then retrieve it
        retrieved_task = task_service.get_task(created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title

    def test_get_task_not_found(self, task_service):
        """Test getting a non-existent task."""
        fake_id = uuid4()
        task = task_service.get_task(fake_id)
        
        assert task is None

    def test_get_tasks_list(self, task_service):
        """Test getting list of tasks."""
        # Create multiple tasks
        tasks_data = [
            TaskCreate(title="Task 1", description="First task", status=TaskStatus.CREATED),
            TaskCreate(title="Task 2", description="Second task", status=TaskStatus.IN_PROGRESS),
            TaskCreate(title="Task 3", description="Third task", status=TaskStatus.COMPLETED),
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            task = task_service.create_task(task_data)
            created_tasks.append(task)
        
        tasks, total = task_service.get_tasks()
        
        # Check that we have at least the tasks we created
        assert len(tasks) >= 3
        assert total >= 3

    def test_get_tasks_with_filtering(self, task_service):
        """Test getting tasks with status filtering."""
        # Create tasks with different statuses
        tasks_data = [
            TaskCreate(title="Task 1", description="First task", status=TaskStatus.CREATED),
            TaskCreate(title="Task 2", description="Second task", status=TaskStatus.IN_PROGRESS),
            TaskCreate(title="Task 3", description="Third task", status=TaskStatus.COMPLETED),
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            task = task_service.create_task(task_data)
            created_tasks.append(task)
        
        # Filter by status
        tasks, total = task_service.get_tasks(status=TaskStatus.CREATED)
        
        # Check that we have at least one task with CREATED status
        assert len(tasks) >= 1
        assert total >= 1
        # Check that all returned tasks have the correct status
        for task in tasks:
            assert task.status == TaskStatus.CREATED

    def test_get_tasks_with_pagination(self, task_service):
        """Test getting tasks with pagination."""
        # Create multiple tasks
        created_tasks = []
        for i in range(15):
            task_data = TaskCreate(
                title=f"Task {i+1}",
                description=f"Task {i+1} description",
                status=TaskStatus.CREATED
            )
            task = task_service.create_task(task_data)
            created_tasks.append(task)
        
        # Test pagination
        tasks, total = task_service.get_tasks(skip=5, limit=5)
        
        assert len(tasks) == 5
        # Check that we have at least 15 tasks total
        assert total >= 15

    def test_update_task(self, task_service):
        """Test updating a task."""
        # First create a task
        task_data = TaskCreate(
            title="Original Task",
            description="Original description",
            status=TaskStatus.CREATED
        )
        created_task = task_service.create_task(task_data)
        
        # Update the task
        update_data = TaskUpdate(
            title="Updated Task",
            description="Updated description",
            status=TaskStatus.IN_PROGRESS
        )
        
        updated_task = task_service.update_task(created_task.id, update_data)
        
        assert updated_task is not None
        assert updated_task.title == update_data.title
        assert updated_task.description == update_data.description
        assert updated_task.status == update_data.status

    def test_update_task_partial(self, task_service):
        """Test partial task update."""
        # First create a task
        task_data = TaskCreate(
            title="Original Task",
            description="Original description",
            status=TaskStatus.CREATED
        )
        created_task = task_service.create_task(task_data)
        
        # Update only title
        update_data = TaskUpdate(title="Updated Task")
        
        updated_task = task_service.update_task(created_task.id, update_data)
        
        assert updated_task is not None
        assert updated_task.title == update_data.title
        assert updated_task.description == created_task.description  # Unchanged
        assert updated_task.status == created_task.status  # Unchanged

    def test_update_task_not_found(self, task_service):
        """Test updating a non-existent task."""
        fake_id = uuid4()
        update_data = TaskUpdate(title="Updated Task")
        
        updated_task = task_service.update_task(fake_id, update_data)
        
        assert updated_task is None

    def test_delete_task(self, task_service):
        """Test deleting a task."""
        # First create a task
        task_data = TaskCreate(
            title="Task to Delete",
            description="This task will be deleted",
            status=TaskStatus.CREATED
        )
        created_task = task_service.create_task(task_data)
        
        # Delete the task
        result = task_service.delete_task(created_task.id)
        
        assert result is True
        
        # Verify task is deleted
        retrieved_task = task_service.get_task(created_task.id)
        assert retrieved_task is None

    def test_delete_task_not_found(self, task_service):
        """Test deleting a non-existent task."""
        fake_id = uuid4()
        result = task_service.delete_task(fake_id)
        
        assert result is False

    def test_task_exists(self, task_service):
        """Test checking if task exists."""
        # Create a task
        task_data = TaskCreate(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        created_task = task_service.create_task(task_data)
        
        # Check if it exists
        assert task_service.task_exists(created_task.id) is True
        
        # Check non-existent task
        fake_id = uuid4()
        assert task_service.task_exists(fake_id) is False
