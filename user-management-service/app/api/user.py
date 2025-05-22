from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.model import User, StudentTransfer
from app.schema.users import UserCreate, UserResponse
from app.schema.student_transfers import StudentTransferCreate, StudentTransferResponse
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return {"error": "user not found"}
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password,  # Use bcrypt in production
        full_name=user.full_name or "",
        status="active",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_username).first()
    if user is None:
        raise  HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None