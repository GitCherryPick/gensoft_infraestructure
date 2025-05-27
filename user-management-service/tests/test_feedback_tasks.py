import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app

client = TestClient(app)

@pytest.fixture
def feedback_data_valid():
    return{
        "student_id": 7, 
        "task_id_lab": 1,
        "task_id_rep": 0,
        "feedback_ai": ["El nombre de la función `factorizar` no coincide con el nombre esperado `factorial`."],
        "feedback_docente": [],
        "n_intentos": 1,
        "estado": "incorrecto"
    }

def test_create_feedback_task(feedback_data_valid):
    response = client.post("/feedback/exercise", json=feedback_data_valid)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["feedback_ai"] == feedback_data_valid["feedback_ai"]
    assert response_data["student_id"] == feedback_data_valid["student_id"]
    assert response_data["task_id_lab"] == feedback_data_valid["task_id_lab"]

def test_create_fedback_task_with_error(feedback_data_valid):
    del(feedback_data_valid["student_id"])    
    response = client.post("/feedback/exercise", json=feedback_data_valid)
    assert response.status_code == 422


