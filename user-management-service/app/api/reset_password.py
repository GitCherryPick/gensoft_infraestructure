from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schema.reset_password import PasswordResetRequest, PasswordResetConfirm
from app.services.reset_password import request_password_reset, confirm_password_reset

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/password-reset/request")
def password_reset_request(data: PasswordResetRequest, db: Session = Depends(get_db)):
    request_password_reset(data.email, db)
    return {"message": "Si el email está registrado, se ha enviado un enlace"}

@router.post("/password-reset/confirm")
def password_reset_confirm(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    if not confirm_password_reset(data.token, data.new_password, db):
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    return {"message": "Contraseña actualizada correctamente"}
