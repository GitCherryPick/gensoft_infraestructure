from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.model.grade import Grade
from app.schema.grade import GradeCreate, GradeUpdate, GradeOut

router = APIRouter(prefix="/grades", tags=["grades"])

def calculate_is_passed(score: int) -> bool:
    return score >= 51

@router.post("/", response_model=GradeOut, status_code=status.HTTP_201_CREATED)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    grade_data = grade.model_dump()

    grade_data["is_passed"] = calculate_is_passed(grade_data["score"])
    existing_grade = db.query(Grade).filter(Grade.user_id == grade_data["user_id"]).first()

    if existing_grade:
        raise HTTPException(status_code=400, detail="User already has a grade assigned")
    db_grade = Grade(**grade_data)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/", response_model=List[GradeOut])
def get_grades(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Grade).offset(skip).limit(limit).all()

@router.get("/{grade_id}", response_model=GradeOut)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade

@router.put("/{grade_id}", response_model=GradeOut)
def update_grade(grade_id: int, grade_update: GradeUpdate, db: Session = Depends(get_db)):
    db_grade = db.query(Grade).get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    
    update_data = grade_update.model_dump(exclude_unset=True)

    if "score" in update_data:
        update_data["is_passed"] = calculate_is_passed(update_data["score"])
    
    for field, value in update_data.items():
        setattr(db_grade, field, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = db.query(Grade).get(grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(db_grade)
    db.commit()
    return None
