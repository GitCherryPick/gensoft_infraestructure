import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
user_data = {
    "username": "testuser3",
    "email": "testuser3@example.com",
    "password": "testpassword",
    "full_name": "Test User"
}

def test_basic_route():    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User Management microservice!"}
    
def test_not_found_route():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_create_user():
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert response_data["full_name"] == user_data["full_name"]
    assert "id" in response_data

def test_delete_user():
    response = client.delete("/users/testuser3")
    assert response.status_code == 200
    
def test_hash_password_format():			#Verificar que hash_password genera hashes de bcrypt válidos
    password = "SecurePass123!"
    hashed = hash_password(password)
    assert hashed.startswith("$2b$")		# Los hashes de bcrypt comienzan con $2b$
    assert len(hashed) > 50
    assert "$2b$12$" in hashed

def test_verify_password_functionality():	#Verificar que verify_password valida correctamente las contraseñas
    password = "SecurePass123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_different_passwords_different_hashes():	#Verificar que contraseñas diferentes generan hashes diferentes
    password1 = "SecurePass123!"
    password2 = "AnotherPass456!"
    hash1 = hash_password(password1)
    hash2 = hash_password(password2)
    assert hash1 != hash2				    # Los hash deben ser diferentes

def test_same_password_different_hashes():	#Verificar que la misma contraseña genera hashes diferentes
    password = "SecurePass123!"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2				    # Los hashes deben ser diferentes
    assert verify_password(password, hash1) is True	# Pero ambos deben validar la misma contraseña
    assert verify_password(password, hash2) is True

def test_user_creation_with_hashed_password():		#Verificar que al crear un usuario, la contraseña se guarda hasheada
    response = client.post("/users/", json=security_test_user)	# Crear un usuario para la prueba
    assert response.status_code == 200
    auth_response = client.post("/auth/login", json=login_data)	# Intentar iniciar sesión con las credenciales correctas
    assert auth_response.status_code == 200
    assert "access_token" in auth_response.json()
    assert "token_type" in auth_response.json()
    assert auth_response.json()["token_type"] == "bearer"

def test_login_with_correct_credentials():	#Verificar que el login funciona con credenciales correctas
    auth_response = client.post("/auth/login", json=login_data)	# Esta prueba asume que el usuario ya fue creado en la prueba anterior
    assert auth_response.status_code == 200
    token_data = auth_response.json()		# Verificar que se devuelve un token válido
    assert "access_token" in token_data
    assert len(token_data["access_token"]) > 0
    assert token_data["token_type"] == "bearer"

def test_login_with_incorrect_credentials():	#Verificar que el login falla con credenciales incorrectas
    auth_response = client.post("/auth/login", json=wrong_login_data)	# Intentar iniciar sesión con una contraseña incorrecta
    assert auth_response.status_code == 401     # Unauthorized
    error_data = auth_response.json()			# Verificar el mensaje de error
    assert "detail" in error_data
    assert "Invalid username or password" in error_data["detail"]


					# Limpieza: eliminar el usuario de prueba después de todas las pruebas
def test_cleanup_security_user():
    response = client.delete(f"/users/{security_test_user['username']}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "deleted successfully" in response.json()["message"]