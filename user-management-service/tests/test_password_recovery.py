import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from jose import jwt
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.token import create_reset_token, verify_reset_token, SECRET_KEY, ALGORITHM
from app.core.security import get_password_hash, verify_password
from app.services.reset_password import confirm_password_reset

client = TestClient(app)

@pytest.fixture
def mock_db():
    mock = MagicMock()
    return mock

@pytest.fixture
def user():
    user = MagicMock()
    user.email = "test@example.com"
    user.username = "testuser"
    user.full_name = "Test User"
    user.status = "active"
    return user

#Test las utilidades de creacion y verificacion de tokens
def test_token_utils():
    email = "test@example.com"
    token = create_reset_token(email)
    decoded_email = verify_reset_token(token)
    assert decoded_email == email
    assert verify_reset_token("invalid-token") is None

#Test que un token expirado no es válido
def test_expired_token():
    expire = datetime.utcnow() - timedelta(hours=1)
    expired_token = jwt.encode(
        {"sub": "test@example.com", "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    assert verify_reset_token(expired_token) is None

#Test para el endpoint de solicitud de restablecimiento de contraseña
def test_request_password_reset_endpoint():

    response = client.post(
        "/auth/password-reset/request",
        json={"email": "test@example.com"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Si el email está registrado, se ha enviado un enlace"}

#Test para el endpoint de confirmación de restablecimiento de contraseña (éxito)
@patch('app.api.reset_password.confirm_password_reset')
def test_confirm_password_reset_endpoint_success(mock_confirm_reset):
    mock_confirm_reset.return_value = True
   
    response = client.post(
        "/auth/password-reset/confirm",
        json={"token": "valid-token", "new_password": "newpassword123"}
    )
   
    assert response.status_code == 200
    assert response.json() == {"message": "Contraseña actualizada correctamente"}
    mock_confirm_reset.assert_called_once()
    args = mock_confirm_reset.call_args[0]
    assert args[0] == "valid-token"
    assert args[1] == "newpassword123"

#Test para el endpoint de confirmación de restablecimiento de contraseña (fallo)
def test_confirm_password_reset_endpoint_failure():
   
    response = client.post(
        "/auth/password-reset/confirm",
        json={"token": "invalid-token", "new_password": "newpassword123"}
    )

    assert response.status_code == 400
    assert "Token inválido o expirado" in response.json()["detail"]

#Test para el servicio de solicitud de restablecimiento de contraseña (usuario existente)
def test_request_password_reset_service_success(mock_db):
    from app.services.reset_password import request_password_reset
   
    user = MagicMock()
    user.email = "test@example.com"
    result = request_password_reset("test@example.com", mock_db)
    assert result is True
   
#Test para el servicio de confirmación de restablecimiento de contraseña (éxito)
def test_confirm_password_reset_service_success(monkeypatch):
    email = "test@example.com"
    token = create_reset_token(email)
    mock_db = MagicMock()

    monkeypatch.setattr("app.repositories.user.update_user_password", lambda e, p, db: True)
    monkeypatch.setattr("app.utils.token.verify_reset_token", lambda t: email)
    result = confirm_password_reset(token, "newpassword123", mock_db)
    assert result is True

#Test para el servicio de confirmación de restablecimiento de contraseña (token inválido)
def test_confirm_password_reset_service_invalid_token(mock_db):
    result = confirm_password_reset("invalid-token", "newpassword123", mock_db)
    assert result is False

#Test para las utilidades de hash y verificación de contraseñas
def test_password_utilities():
    password = "plaintext_password"
    hashed = get_password_hash(password)

    assert isinstance(hashed, str)
    assert len(hashed) > 0
    result = verify_password(password, hashed)
    assert result is True