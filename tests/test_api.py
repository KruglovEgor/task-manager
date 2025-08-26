"""API endpoint tests."""

import pytest
from fastapi import status
from uuid import uuid4

from app.models.task import TaskStatus


class TestTaskAPI:
    """Test cases for task API endpoints."""

    def test_create_task_success(self, client):
        """Test successful task creation."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "создано"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_status(self, client):
        """Test task creation without status (should default to 'создано')."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "создано"

    def test_create_task_invalid_data(self, client):
        """Test task creation with invalid data."""
        # Empty title
        task_data = {
            "title": "",
            "description": "This is a test task"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Missing title
        task_data = {
            "description": "This is a test task"
        }
        
        response = client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_task_success(self, client):
        """Test successful task retrieval."""
        # First create a task
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "создано"
        }
        
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]

    def test_get_task_not_found(self, client):
        """Test task retrieval with non-existent ID."""
        fake_id = str(uuid4())
        response = client.get(f"/api/v1/tasks/{fake_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_tasks_list(self, client):
        """Test getting list of tasks."""
        # Create multiple tasks
        tasks_data = [
            {"title": "Task 1", "description": "First task", "status": "создано"},
            {"title": "Task 2", "description": "Second task", "status": "в работе"},
            {"title": "Task 3", "description": "Third task", "status": "завершено"},
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            response = client.post("/api/v1/tasks/", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())
        
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Check that we have at least the tasks we created
        assert len(data["tasks"]) >= 3
        assert data["total"] >= 3
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_get_tasks_with_filtering(self, client):
        """Test getting tasks with status filtering."""
        # Create tasks with different statuses
        tasks_data = [
            {"title": "Task 1", "description": "First task", "status": "создано"},
            {"title": "Task 2", "description": "Second task", "status": "в работе"},
            {"title": "Task 3", "description": "Third task", "status": "завершено"},
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            response = client.post("/api/v1/tasks/", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())
        
        # Filter by status
        response = client.get("/api/v1/tasks/?status=создано")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Check that we have at least one task with "создано" status
        assert len(data["tasks"]) >= 1
        # Check that all returned tasks have the correct status
        for task in data["tasks"]:
            assert task["status"] == "создано"

    def test_get_tasks_with_pagination(self, client):
        """Test getting tasks with pagination."""
        # Create multiple tasks
        created_tasks = []
        for i in range(15):
            task_data = {
                "title": f"Task {i+1}",
                "description": f"Task {i+1} description",
                "status": "создано"
            }
            response = client.post("/api/v1/tasks/", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())
        
        # Test pagination
        response = client.get("/api/v1/tasks/?skip=5&limit=5")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["tasks"]) == 5
        assert data["skip"] == 5
        assert data["limit"] == 5
        # Check that we have at least 15 tasks total
        assert data["total"] >= 15

    def test_update_task_success(self, client):
        """Test successful task update."""
        # First create a task
        task_data = {
            "title": "Original Task",
            "description": "Original description",
            "status": "создано"
        }
        
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "status": "в работе"
        }
        
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]

    def test_update_task_partial(self, client):
        """Test partial task update."""
        # First create a task
        task_data = {
            "title": "Original Task",
            "description": "Original description",
            "status": "создано"
        }
        
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        # Update only title
        update_data = {"title": "Updated Task"}
        
        response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == task_data["description"]  # Unchanged
        assert data["status"] == task_data["status"]  # Unchanged

    def test_update_task_not_found(self, client):
        """Test task update with non-existent ID."""
        fake_id = str(uuid4())
        update_data = {"title": "Updated Task"}
        
        response = client.put(f"/api/v1/tasks/{fake_id}", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_success(self, client):
        """Test successful task deletion."""
        # First create a task
        task_data = {
            "title": "Task to Delete",
            "description": "This task will be deleted",
            "status": "создано"
        }
        
        create_response = client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/v1/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self, client):
        """Test task deletion with non-existent ID."""
        fake_id = str(uuid4())
        response = client.delete(f"/api/v1/tasks/{fake_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
