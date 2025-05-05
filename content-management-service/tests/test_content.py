from fastapi.testclient import TestClient
from app.main import app  # ajustá el import si tu main.py está en otra ruta

client = TestClient(app)

def test_basic_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Content Management microservice!"}
