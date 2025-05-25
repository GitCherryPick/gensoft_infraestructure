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

def test_loop_execution():
    code = "for i in range(3):\n    print(f'Iteration {i}')"
    response = client.post("/run", json={"code": code})
    assert response.status_code == 200
    response_data = response.json()
    expected_output = "Iteration 0\nIteration 1\nIteration 2\n"
    assert response_data["output"] == expected_output
    assert response_data["errors"] == ""

def test_with_call():
    code = "def hi2():\n    print('hola')"
    call = "5+5"
    response = client.post("/execute", json={"code": code, "call": call})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == "10\n"
    assert response_data["error"] == ""

def test_with_code_error():
    code = "def hi():\n    return 3+3+j"
    call = "hi()"
    response = client.post("/execute", json={"code": code, "call": call})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == ""
    assert "NameError" in response_data["error"]

def test_with_call_error():
    code = "def hi():\n    return 3+3+5"
    call = "hi(5)"
    response = client.post("/execute", json={"code": code, "call": call})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == ""
    assert "TypeError" in response_data["error"]

def test_withTimeout():
    code = "import time\ntime.sleep(5)"
    call = "5+5"
    response = client.post("/execute", json={"code": code, "call": call})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"] == ""
    assert "TimeOut" in response_data["error"]
