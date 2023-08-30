from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.user.model import Base
from app.db.session import get_db
from app.controllers.auth import AuthHandler

client = TestClient(app)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

auth_handler = AuthHandler()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        ({"email": "test@example.com", "password": "testpassword"}, 200),
        ({"email": "test@example.com", "password": "testpassword"}, 400),
    ],
)
def test_register(user_data, expected_status):
    response = client.post("/user/register", json=user_data)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        ({"email": "test@example.com", "password": "testpassword"}, 200),
        ({"email": "wrong@example.com", "password": "testpassword"}, 401),
        ({"email": "test@example.com", "password": "wrongpassword"}, 401),
    ],
)
def test_login(user_data, expected_status):
    response = client.post("/user/login", json=user_data)
    assert response.status_code == expected_status
