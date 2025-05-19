from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.model import User, StudentTransfer, Institution, Role, UserRoles, StudentTransfer 
from app.schema.users import UserCreate, UserResponse
from app.schema.institutions import InstitutionCreate, InstitutionResponse
from app.schema.student_transfers import StudentTransferCreate, StudentTransferResponse
from app.schema.reset_password import PasswordResetRequest, PasswordResetConfirm
from app.api import institutions
from app.model.base import Base
from app.api.reset_password import router as reset_password_router
from app.api import auth 
import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(institutions.router)
app.include_router(reset_password_router, prefix="/auth", tags=["auth"])

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to User Management microservice!"}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return {"error": "user not found"}
    return user

@app.post("/users/", response_model=UserResponse)
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

@app.post("/student_transfers", response_model=StudentTransferResponse)
def create_student_transfer(transfer: StudentTransferCreate, db: Session = Depends(get_db)):
    db_transfer = StudentTransfer(**transfer.model_dump())
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

@app.get("/student_transfers/{transfer_id}", response_model=StudentTransferResponse)
def get_student_transfer(transfer_id: int, db: Session = Depends(get_db)):
    transfer = db.query(StudentTransfer).filter(StudentTransfer.id == transfer_id).first()
    if transfer is None:
        return {"error": "student transfer not found"}
    return transfer

@app.delete("/users/{user_username}")
def delete_user(user_username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_username).first()
    if user is None:
        return {"error": "user not found"}
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}