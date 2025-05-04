from fastapi import APIRouter, HTTPException
from app.schema.reset_password import PasswordResetRequest, PasswordResetConfirm
from app.services.reset_password import request_password_reset, confirm_password_reset

router = APIRouter()

@router.post("/password-reset/request")
def password_reset_request(data: PasswordResetRequest):
    request_password_reset(data.email)
    return {"message": "Si el email está registrado, se ha enviado un enlace"}

@router.post("/password-reset/confirm")
def password_reset_confirm(data: PasswordResetConfirm):
    if not confirm_password_reset(data.token, data.new_password):
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    return {"message": "Contraseña actualizada correctamente"}
