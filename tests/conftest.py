"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.connection import get_db
from app.database.models import Base
from app.models.task import Task, TaskStatus


# We'll create a new engine for each test to ensure isolation


@pytest.fixture(scope="function")
def client():
    """Create a test client with database cleanup after each test."""
    from app.database.connection import engine, SessionLocal
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    
    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up - delete all data from tables
    db = SessionLocal()
    try:
        # Delete all tasks
        db.query(Base.metadata.tables['tasks']).delete()
        db.commit()
    finally:
        db.close()
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.CREATED
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks for testing."""
    return [
        Task(
            title="Task 1",
            description="First test task",
            status=TaskStatus.CREATED
        ),
        Task(
            title="Task 2",
            description="Second test task",
            status=TaskStatus.IN_PROGRESS
        ),
        Task(
            title="Task 3",
            description="Third test task",
            status=TaskStatus.COMPLETED
        ),
    ]
