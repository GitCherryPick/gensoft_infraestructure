import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

task_data = {
  "title": "Condicional if",
  "description": "Este condicional usualmente viene acompanied con un else y else if, en python se utiliza una palabra clave diferente 'elif', es tu oportunidad de trabajar con este nuevo conocimiento.",
  "expected_code": "this_year = 2025\nif(this_year > 2000):\n    return 'welcome new era'\nelif(this_year > 3000):\n    return 'Es el futuro'\nelse:\n    return 'welcome past'",
}
task_data_id = 0

def test_create_task():
    response = client.post("/taskcode", json=task_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["expected_code"] == task_data["expected_code"]
    assert "id" in response_data
    global task_data_id 
    task_data_id = response_data["id"]
    print("llegue aqui", task_data_id)

def test_get_task():
    response = client.get(f"/taskcode/{task_data_id}")
    assert response.status_code == 200

def test_update_task():
    updated_data = {
        "title": "Condicional if",
        "description": "Este condicional usualmente viene acompanied con un else y else if, en python se utiliza una palabra clave diferente 'elif', es tu oportunidad de trabajar con este nuevo conocimiento.",
        "expected_code": "this_year = 2025\nif(this_year > 2000):\n    return 'welcome new era'\nelif(this_year > 3000):\n    return 'Es el futuro'\nelse:\n    return 'welcome past'",
        "template_code": "this_year = 2025\nif(this_year > 2000):\n    return 'welcome new era'\nelif(this_yea"
    }
    response = client.put(f"/taskcode/{task_data_id}", json=updated_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]    
    assert response_data["template_code"] == updated_data["template_code"]

def test_compare_code_correct():
    example_submission = {
        "task_replicator_id": task_data_id,
        "student_code": "this_year = 2025\nif(this_year > 2000):\n    return 'welcome new era'\nelif(this_year > 3000):\n    return 'Es el futuro'\nelse:\n    return 'welcome past'"
    }
    response = client.post("/codereplicated", json=example_submission)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["result"] == "Tarea completada con exito"

def test_compare_code_incorrect():
    example_submission = {
        "task_replicator_id": task_data_id,
        "student_code": "this_year = 2025\nif(this_year2000):\n    return 'welcome new era'\nelif(this_year > 3000):\n    return 'Es el futuro'\nelse:\n    return 'welcome past'"
    }
    response = client.post("/codereplicated", json=example_submission)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["result"] == "Incorrecto"

def test_compare_code_indent_incorrect():
    example_submission = {
        "task_replicator_id": task_data_id,
        "student_code": "this_year = 2025\nif(this_year > 2000):\n  return 'welcome new era'\nelif(this_year > 3000):\n return 'Es el futuro'\nelse:\n  return 'welcome past'"
    }
    response = client.post("/codereplicated", json=example_submission)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["result"] == "Incorrecto"

def test_obtain_template():
    template =  "this_year = 2025\nif(this_year > 2000):\n    return 'welcome new era'\nelif(this_yea"
    response = client.get(f"/taskcode/{task_data_id}/template")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["template_code"] == template    

def test_delete_task():
    response = client.delete(f"/taskcode/{task_data_id}")
    assert response.status_code == 200
 


