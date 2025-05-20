import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_user():
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123",
        "full_name": "Test User",
        "status": "active"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 200
    return res.json()

@pytest.fixture(scope="module")
def created_grade(test_user):
    payload = {
        "user_id": test_user["id"],
        "score": 49
    }
    res = client.post("/grades/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["is_passed"] == False
    return data

def test_list_grades(created_grade):
    res = client.get("/grades/")
    assert res.status_code == 200
    lst = res.json()
    assert any(s["grade_id"] == created_grade["grade_id"] for s in lst)

def test_get_grade(created_grade):
    grade_id = created_grade["grade_id"]
    res = client.get(f"/grades/{grade_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["user_id"] == created_grade["user_id"]
    assert data["is_passed"] == created_grade["is_passed"]
    assert data["score"] == created_grade["score"]

def test_update_grade_auto_passed(created_grade):
    grade_id = created_grade["grade_id"]
    update = {"score": 75}
    res = client.put(f"/grades/{grade_id}", json=update)
    assert res.status_code == 200
    data = res.json()
    assert data["score"] == 75
    assert data["is_passed"] == True

def test_create_grade_with_invalid_score(test_user):
    payload = {
        "user_id": test_user["id"],
        "score": 101
    }
    res = client.post("/grades/", json=payload)
    assert res.status_code == 422 # Validation error

def test_create_duplicate_user_grade(test_user):
    payload = {
        "user_id": test_user["id"],
        "score": 60
    }   
    res = client.post("/grades/", json=payload)
    assert res.status_code == 400 # User already has a grade
    assert "User already has a grade" in res.json()["detail"]

def test_delete_grade(created_grade):
    grade_id = created_grade["grade_id"]
    res = client.delete(f"/grades/{grade_id}")
    assert res.status_code == 204

    res = client.get(f"/grades/{grade_id}")
    assert res.status_code == 404

def test_delete_user():
    response = client.delete("/users/testuser2")
    assert response.status_code == 204