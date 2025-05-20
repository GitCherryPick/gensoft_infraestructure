import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
stat_data = {
    "student_id": 1,
    "total_activities_answered": 0,
    "common_mistakes": ["math_exercises"],
    "interests": [],
    "performance_stats": {"math": 0, "english": 0}
}
stat_data_id = 0

def test_not_found_route():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_create_user():
    response = client.post("/student-stats", json=stat_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["student_id"] == stat_data["student_id"]
    assert response_data["total_activities_answered"] == 0
    assert "last_accessed" in response_data
    global stat_data_id
    stat_data_id = response_data["id"]

def test_get_user():
    response = client.get(f"/student-stats/{stat_data_id}")
    assert response.status_code == 200
    assert response.json()["student_id"] == stat_data["student_id"]
    assert response.json()["total_activities_answered"] == stat_data["total_activities_answered"]
    assert response.json()["common_mistakes"] == stat_data["common_mistakes"]
    assert response.json()["interests"] == stat_data["interests"]
    assert response.json()["performance_stats"] == stat_data["performance_stats"]

def test_update_user():
    update_data = {
        "total_activities_answered": 5,
        "common_mistakes": ["math_exercises", "reading"],
        "interests": ["science", "history"],
        "performance_stats": {"math": 1, "english": 0.5}
    }
    response = client.put(f"/student-stats/{stat_data_id}", json=update_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["student_id"] == stat_data["student_id"]
    assert response.json()["total_activities_answered"] == update_data["total_activities_answered"]
    assert response.json()["common_mistakes"] == update_data["common_mistakes"]
    assert response.json()["interests"] == update_data["interests"]
    assert response.json()["performance_stats"] == update_data["performance_stats"]

def test_delete_user():
    response = client.delete(f"/student-stats/{stat_data_id}")
    assert response.status_code == 200
    