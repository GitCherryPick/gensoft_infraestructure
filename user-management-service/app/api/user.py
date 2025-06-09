from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.model import User, StudentTransfer
from app.model.roles import Role
from app.model.user_roles import UserRoles
from app.schema.users import UserCreate, UserResponse
from app.schema.student_transfers import StudentTransferCreate, StudentTransferResponse
from app.database import get_db
from app.utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users-students")
def obtain_users_students(db: Session = Depends(get_db)):
    query = (
        db.query(User)
        .join(UserRoles, User.id == UserRoles.user_id)
        .join(Role, UserRoles.role_id == Role.id)
        .filter(Role.name == "estudiante")
    )
    students = query.all()
    return students

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
    
    rol = db.query(Role).filter(Role.name == user.role)[0]
    print("encontr el rol  ", rol)
    
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name or "",
        status="active",
    )

    if (not rol) :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No existe el rol"
        )

    # Consulta ORM normal
    # roles = db.query(Role).all()
    # print("ORM roles:", roles)

    # tip = db.query(User).all()
    # print("ORM users:", tip)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        user_role = UserRoles(
            user_id=db_user.id,
            role_id=rol.id
        )
        db.add(user_role)
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

@router.post("/batch_users")
def obtain_users_by_ids(users_ids: List[int], db: Session = Depends(get_db)):
    users = db.query(User).filter(User.id.in_(users_ids)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return [{"id": user.id, "name": user.full_name} for user in users]
