from ..utils.token import create_reset_token, verify_reset_token
from ..repositories.user import get_user_by_email, update_user_password
from ..utils.email import send_email  # deberás implementar esto

def request_password_reset(email: str):
    user = get_user_by_email(email)
    if not user:
        return False 
    token = create_reset_token(email)
    reset_link = f"{"http://localhost:3000"}/reset-password?token={token}"
    send_email(email, "Restablecer contraseña", f"Enlace: {reset_link}")
    return True

def confirm_password_reset(token: str, new_password: str):
    email = verify_reset_token(token)
    if not email:
        return False
    return update_user_password(email, new_password)
