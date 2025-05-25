import pytest
from unittest.mock import patch

@pytest.fixture
def task_with_tests(client):
    task_data = {
        "title": "Suma dos números",
        "enunciado": "Implementa suma.",
        "tests": [
            {"input": "suma(1, 2)", "output": "3"},
            {"input": "suma(3, 4)", "output": "7"}
        ]
    }
    response = client.post("/tasks", json=task_data)
    return response.json()["task_id"]

@patch("app.api.routes.execute_code")  
def test_enviar_correct_code(mock_execute, client, task_with_tests):
    mock_execute.side_effect = [
        {"output": "3\n", "error": ""},
        {"output": "7\n", "error": ""}
    ]

    payload = {
        "code": "def suma(a, b): return a + b",
        "taskId": task_with_tests
    }

    response = client.post("/enviar", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["generalVeredict"] == "Accepted"
    assert len(data["testCases"]) == 2
