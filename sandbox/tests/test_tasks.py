import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

task_payload = {
    "title": "Suma simple",
    "enunciado": "Implementa una función llamada suma que reciba dos enteros y retorne su suma.",
    "tests": [
        {"input": "suma(1, 2)", "output": "3"},
        {"input": "suma(5, 7)", "output": "12"},
        {"input": "suma(0, 0)", "output": "0"}
    ]
}

task_id = None

def test_create_task():
    global task_id
    response = client.post("/tasks", json=task_payload)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    task_id = data["task_id"]
    assert data["message"] == "Tarea creada con éxito"

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id():
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_payload["title"]
    assert len(data["tests"]) == 3

def test_update_task():
    updated_task = {
        "title": "Suma modificada",
        "enunciado": "Modifica la función suma para que reste."
    }
    response = client.put(f"/tasks/{task_id}", json=updated_task)
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea actualizada correctamente"

def test_add_test_to_task():
    new_test = {"input": "suma(10, 10)", "output": "20"}
    response = client.post(f"/tasks/{task_id}/tests", json=new_test)
    assert response.status_code == 200
    assert "test_id" in response.json()

def test_enviar_code_success():
    correct_code = """
def suma(a, b):
    return a + b
"""
    submission = {"code": correct_code, "taskId": task_id}
    response = client.post("/enviar", json=submission)
    assert response.status_code == 200
    data = response.json()
    assert data["generalVeredict"] == "Accepted"
    assert all(tc["veredict"] == "Accepted" for tc in data["testCases"])

def test_enviar_code_wrong_answer():
    wrong_code = """
def suma(a, b):
    return a - b
"""
    submission = {"code": wrong_code, "taskId": task_id}
    response = client.post("/enviar", json=submission)
    assert response.status_code == 200
    data = response.json()
    assert data["generalVeredict"] == "Error"
    assert any(tc["veredict"] == "Wrong Answer" for tc in data["testCases"])

def test_enviar_code_error():
    error_code = """
def suma(a, b)
    return a + b
"""
    submission = {"code": error_code, "taskId": task_id}
    response = client.post("/enviar", json=submission)
    assert response.status_code == 200
    data = response.json()
    assert data["generalVeredict"] == "Error"
    assert any(tc["veredict"] == "Error" for tc in data["testCases"])

def test_delete_test():
   
    response = client.get(f"/tasks/{task_id}")
    test_id = response.json()["tests"][0]["id"]
    delete_response = client.delete(f"/tests/{test_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Test eliminado correctamente"

def test_delete_task():
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea eliminada correctamente"
