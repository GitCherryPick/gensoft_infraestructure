import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_user():
    user_data = {
        "username": "testuser4",
        "email": "test4@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "status": "active",
        "role": "estudiante"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 200
    return res.json()

@pytest.fixture(scope="module")
def feedback_data_valid(test_user):
    return{
        "student_id": test_user["id"], 
        "task_id_lab": 1,
        "task_id_rep": 0,
        "feedback_ai": ["El nombre de la función `factorizar` no coincide con el nombre esperado `factorial`."],
        "feedback_docente": [],
        "n_intentos": 1,
        "estado": "incorrecto"
    }

@pytest.fixture(scope="module")
def test_create_feedback_task(feedback_data_valid):
    response = client.post("/feedback/exercise", json=feedback_data_valid)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["feedback_ai"] == feedback_data_valid["feedback_ai"]
    assert response_data["student_id"] == feedback_data_valid["student_id"]
    assert response_data["task_id_lab"] == feedback_data_valid["task_id_lab"]
    return response_data

def test_create_feedback_task_with_error():
    new_data =  {
        "task_id_lab": 1,
        "task_id_rep": 0,
        "feedback_ai": ["El nombre de la función `factorizar` no coincide con el nombre esperado `factorial`."],
        "feedback_docente": [],
        "n_intentos": 1,
        "estado": "incorrecto"
    }  
    response = client.post("/feedback/exercise", json=new_data)
    assert response.status_code == 422

def test_delete_feedback_task(test_create_feedback_task):
    id_feedback = test_create_feedback_task["id"]
    response = client.delete(f"/feedback/exercise/{id_feedback}")
    assert response.status_code == 200
    
def test_delete_user():
    response = client.delete("/users/testuser4")
    assert response.status_code == 204
