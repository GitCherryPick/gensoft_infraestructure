import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
user_data = {
    "username": "testuser3",
    "email": "testuser3@example.com",
    "password": "testpassword",
    "full_name": "Test User",
    "role": "estudiante"
}

def test_basic_route():    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User Management microservice!"}
    
def test_not_found_route():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_create_user():
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["full_name"] == user_data["full_name"]
    assert "id" in response_data

def test_delete_user():
    response = client.delete("/users/testuser3")
    assert response.status_code == 204
