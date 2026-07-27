"""Módulo de configuración y fixtures de Pytest para pruebas automáticas."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.database import Base
from src.dependencies import get_db
from src.main import app
from src.models import Task, User

# Base de datos en memoria SQLite aislada para ejecución rápida de pruebas
TEST_DATABASE_URL = "sqlite:///:memory:"

# StaticPool mantiene la misma conexión en memoria compartida entre hilos en SQLite
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, bind=engine_test)


@pytest.fixture()
def db_session():
    """Genera una sesión de base de datos limpia creando y destruyendo tablas por test."""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client(db_session):
    """Cliente de pruebas HTTP que sobrescribe la dependencia de base de datos global."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, base_url="https://testserver") as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_client(client):
    """Cliente HTTP pre-autenticado con un usuario de prueba registrado y logueado."""
    payload = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword"
    }
    client.post("/users/register", json=payload)
    client.post("/users/login", data={"username": "testuser@test.com", "password": "testpassword"})
    return client