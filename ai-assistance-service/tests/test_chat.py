import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

question_data = {
    "question": "What is the capital of France?"
}

conversate_data = {
    "user_id": "12345",
    "question_text": "Tell me a joke.",
    "important": True
}

def test_ask_ai():
    response = client.post("/ai/ask", json=question_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_conversate_ai():
    response = client.post("/ai/chat", json=conversate_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["answer"] is not None
    assert response.json()["question"] == conversate_data["question_text"]