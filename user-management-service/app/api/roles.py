from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db

from app.schema.roles import RoleBase, RoleResponse
from app.model import Role
router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_roles(sub: RoleBase, db: Session = Depends(get_db)):
    
    db_sub = Role(**sub.model_dump())

    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("/", response_model=List[RoleResponse])
def get_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    print("ORM roles:", roles)
    return db.query(Role).offset(skip).limit(limit).all()
