import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_if_program():
    code = "if (1>12):\n    print('hola')\nelse:\n  print('hola:c')"
    response = client.post("/run", json={"code": code})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == "hola:c\n"
    assert response_data["errors"] == ""

def test_error_program():
    code = "if (1>12): print('hola') else: print('hola:c')"
    response = client.post("/run", json={"code": code})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == ""
    assert "SyntaxError" in response_data["errors"]

