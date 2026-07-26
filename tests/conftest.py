import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base
from src.models import User, Task
from src.domains.users.dependencies import get_db


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

    def overryide_get_db():
        yield db_session

    app.dependency_overrides[get_db] = overryide_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()