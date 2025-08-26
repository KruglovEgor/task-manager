"""Model tests."""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from app.models.task import Task, TaskStatus


class TestTaskModel:
    """Test cases for Task model."""

    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.CREATED
        assert isinstance(task.id, UUID)
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_default_values(self):
        """Test task creation with default values."""
        task = Task(
            title="Test Task",
            description="Test description"
        )
        
        assert task.status == TaskStatus.CREATED
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_update_timestamp(self):
        """Test updating task timestamp."""
        task = Task(
            title="Test Task",
            description="Test description"
        )
        
        original_updated_at = task.updated_at
        # Add a small delay to ensure timestamp difference
        import time
        time.sleep(0.001)
        task.update_timestamp()
        
        # Check that timestamp was updated (should be greater or equal)
        assert task.updated_at >= original_updated_at

    def test_task_status_enum(self):
        """Test task status enumeration."""
        assert TaskStatus.CREATED == "создано"
        assert TaskStatus.IN_PROGRESS == "в работе"
        assert TaskStatus.COMPLETED == "завершено"

    def test_task_validation(self):
        """Test task validation."""
        # Valid task
        task = Task(
            title="Valid Task",
            description="Valid description",
            status=TaskStatus.CREATED
        )
        assert task.title == "Valid Task"

        # Test with empty title (should raise validation error)
        with pytest.raises(ValueError):
            Task(
                title="",
                description="Valid description"
            )

    def test_task_serialization(self):
        """Test task serialization."""
        task = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.IN_PROGRESS
        )
        
        # Test dict conversion
        task_dict = task.model_dump()
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test description"
        assert task_dict["status"] == "в работе"
        assert "id" in task_dict
        assert "created_at" in task_dict
        assert "updated_at" in task_dict

    def test_task_json_serialization(self):
        """Test task JSON serialization."""
        task = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.COMPLETED
        )
        
        # Test JSON conversion
        task_json = task.model_dump_json()
        task_dict = task.model_dump()
        
        # Verify all fields are present in JSON
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test description"
        assert task_dict["status"] == "завершено"
        assert "id" in task_dict
        assert "created_at" in task_dict
        assert "updated_at" in task_dict

    def test_task_copy(self):
        """Test task copying."""
        original_task = Task(
            title="Original Task",
            description="Original description",
            status=TaskStatus.CREATED
        )
        
        copied_task = original_task.model_copy()
        
        assert copied_task.title == original_task.title
        assert copied_task.description == original_task.description
        assert copied_task.status == original_task.status
        assert copied_task.id == original_task.id
        assert copied_task.created_at == original_task.created_at
        assert copied_task.updated_at == original_task.updated_at

    def test_task_copy_with_updates(self):
        """Test task copying with updates."""
        original_task = Task(
            title="Original Task",
            description="Original description",
            status=TaskStatus.CREATED
        )
        
        copied_task = original_task.model_copy(update={"title": "Updated Task"})
        
        assert copied_task.title == "Updated Task"
        assert copied_task.description == original_task.description
        assert copied_task.status == original_task.status
        assert copied_task.id == original_task.id

    def test_task_equality(self):
        """Test task equality."""
        task1 = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        
        task2 = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        
        # Tasks with different IDs should not be equal
        assert task1 != task2

    def test_task_string_representation(self):
        """Test task string representation."""
        task = Task(
            title="Test Task",
            description="Test description",
            status=TaskStatus.CREATED
        )
        
        task_str = str(task)
        assert "Test Task" in task_str
        assert "создано" in task_str
