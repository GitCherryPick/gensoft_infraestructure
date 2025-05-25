def test_create_task(client):
    task_data = {
        "title": "Suma dos números",
        "enunciado": "Implementa una función que sume dos números.",
        "tests": [
            {"input": "suma(1, 2)", "output": "3"},
            {"input": "suma(10, 20)", "output": "30"}
        ]
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["message"] == "Tarea creada con éxito"

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_task(client):
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Suma dos números"
    assert len(data["tests"]) == 2

def test_update_task(client):
    update_data = {
        "title": "Suma actualizada",
        "enunciado": "Modifica la función suma."
    }
    response = client.put("/tasks/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea actualizada correctamente"

def test_delete_task(client):
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea eliminada correctamente"
