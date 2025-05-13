from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import student_stats as crud
from app.schema.student_stats import StudentStatsRequest,StudentStatsUpdateRequest, StudentStatsResponse
from app.database import get_db  
from app.model.student_stats import StudentStats

router = APIRouter()

@router.post("/", response_model=StudentStatsResponse)
def create(stats: StudentStatsRequest, db: Session = Depends(get_db)):
    return crud.create_student_stats(db, stats)

@router.get("/", response_model=List[StudentStatsResponse])
def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all student stats
    """
    try:
        stats = db.query(StudentStats).offset(skip).limit(limit).all()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener contenidos: {str(e)}")

@router.get("/{id}", response_model=StudentStatsResponse)
def read(id: int, db: Session = Depends(get_db)):
    stats = crud.get_student_stats(db, id)
    if not stats:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return stats


@router.put("/{id}", response_model=StudentStatsResponse)
def update(id: int, stats: StudentStatsUpdateRequest, db: Session = Depends(get_db)):
    updated = crud.update_student_stats(db, id, stats)
    if not updated:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return updated


@router.delete("/{id}", response_model=StudentStatsResponse)
def delete(id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student_stats(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return deleted
