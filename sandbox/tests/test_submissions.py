import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_submission():
    response = client.post("/submissions/", json={
        "user_id": 1,
        "code": "print(Hello World)"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["code"] == "print(Hello World)"
    assert data["result"] == "pending"