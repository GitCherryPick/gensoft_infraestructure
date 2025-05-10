import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

user_data = {
    "username": "testuser5",
    "password_hash": "testpassword"  
}

def test_user_creation():
    response = client.post("/users/", json=user_data)
    assert response.status_code in [200, 201]

def test_login_success():

    login_data = {
        "username": user_data["username"],
        "password": "testpassword"  # Test en caso de que sea exitoso el login
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure_wrong_password():   # Test en caso de que la contraseña sea incorrecta

    login_data = {
        "username": user_data["username"],
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_login_failure_user_not_found():   # Test en caso de que el usuario no exite

    login_data = {
        "username": "nonexistentuser",
        "password": "irrelevant"
    }

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_test_route():           # Test paara probar que /auth/test responde correctamente
    response = client.post("/auth/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Test successful"}
