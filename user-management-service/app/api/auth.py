from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
import json
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.database import get_db
from app.model import User
from app.utils.security import create_access_token, verify_password, get_password_hash
from app.schema.token import LoginRequest, Token, TokenData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    if not login_data.username or not login_data.password:
        logger.warning(f"Intento de login con campos vacíos desde {request.client.host}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre de usuario y contraseña son requeridos",
        )
    
    user = db.query(User).filter(User.username == login_data.username).first()
    
    error_detail = "Credenciales inválidas"
    
    if not user:
        logger.warning(f"Intento de login con usuario inexistente: {login_data.username} desde {request.client.host}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.status != "active":
        logger.warning(f"Intento de login de usuario inactivo: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Por favor, contacte al administrador.",
        )
    
    try:
        if not verify_password(login_data.password, user.password_hash):
            logger.warning(f"Contraseña incorrecta para el usuario: {user.username} desde {request.client.host}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_detail,
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        logger.error(f"Error al verificar la contraseña para {user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la autenticación",
        )
    
    try:
        user.last_login = datetime.utcnow()
        db.commit()
        logger.info(f"Login exitoso para el usuario: {user.username}")
    except Exception as e:
        logger.error(f"Error al actualizar último login para {user.username}: {str(e)}")
    
    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "email": user.email
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=2003)
    )
    
    response = {
        "access_token": access_token, 
        "token_type": "bearer"
    }
    
    user_data = {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name or ""
    }
    
    response_headers = {
        "X-User-Data": json.dumps(user_data, ensure_ascii=False)
    }
    
    return JSONResponse(
        content=response,
        headers=response_headers
    )

@router.post("/test")
def test():
    return {"message": "Test successful"}