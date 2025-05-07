from sqlalchemy.orm import Session
from ..utils.token import create_reset_token, verify_reset_token
from ..repositories.user import get_user_by_email, update_user_password
from ..utils.email import send_email  # deberás implementar esto

def request_password_reset(email: str, db: Session):
    user = get_user_by_email(email, db)
    if not user: 
        return False 
    token = create_reset_token(email)
    reset_link = f"http://localhost:3000/recover-password/password-reset-card?token={token}"
    send_email(email, "Restablecer contraseña", f"{reset_link}")
    return True

def confirm_password_reset(token: str, new_password: str, db: Session):
    email = verify_reset_token(token)
    print(f"this is the {email}")
    if not email:
        return False
    return update_user_password(email, new_password, db)
