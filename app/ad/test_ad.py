from fastapi.testclient import TestClient
from app.controllers.auth import AuthHandler
from unittest.mock import patch
import pytest
from app.main import app

client = TestClient(app)

auth_handler = AuthHandler()


def override_auth_dependency(*args, **kwargs):
    return {"user_id": 1, "email": "test@test.com"}, {}


app.dependency_overrides[auth_handler.check_current_user_tokens] = override_auth_dependency


@pytest.mark.parametrize(
    "ad_data, expected_status, expected_response",
    [
        ({"title": "Test Ad", "content": "This is a test ad"}, 200, {"title": "Test Ad"}),
    ],
)
def test_create_ad(ad_data, expected_status, expected_response):
    with patch("app.controllers.auth.auth_handler.check_current_user_tokens", override_auth_dependency):
        response = client.post("/ad/create", json=ad_data)
    assert response.status_code == 200, response.content
    assert "id" in response.json()
    assert response.json()["title"] == "Test Ad"
    assert response.json()["content"] == "This is a test ad"


def test_edit_ad():
    data = {"title": "Edited Ad", "content": "This ad has been edited"}
    response = client.put("/ad/edit/1", json=data)
    assert response.status_code == 200
    assert response.json()["title"] == "Edited Ad"


def test_delete_ad():
    response = client.delete("/ad/delete/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Ad deleted successfully"


def test_list_ads():
    response = client.get("/ad/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_user_ads():
    response = client.get("/ad/user_ads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
