import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base
from src.models import User, Task
from src.domains.users.dependencies import get_db as user_get
from src.domains.tasks.dependencies import get_db as task_get


TEST_DATABASE_URL = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing

engine_test = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, bind=engine_test)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[user_get] = override_get_db
    app.dependency_overrides[task_get] = override_get_db
  
    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_client(client):
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"
    }
    client.post("/users/register", json=payload)
    client.post("/users/login", data={"username": "testuser@test.com", "password": "testpassword"})
    return client