import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/register", json={"email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_update_user():
    # Assuming a user with ID 'some_user_id' exists
    response = client.put("/users/some_user_id", json={"email": "updated@example.com", "password": "newpass"})
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"

def test_delete_user():
    # Assuming a user with ID 'some_user_id' exists
    response = client.delete("/users/some_user_id")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"