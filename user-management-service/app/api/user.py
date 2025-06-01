from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.model import User, StudentTransfer
from app.schema.users import UserCreate, UserResponse
from app.schema.student_transfers import StudentTransferCreate, StudentTransferResponse
from app.database import get_db
from app.utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return {"error": "user not found"}
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está en uso"
        )
    
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name or "",
        status="active",
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

@router.delete("/{user_username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_username).first()
    if user is None:
        raise  HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None