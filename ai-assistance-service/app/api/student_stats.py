from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import student_stats as crud
from app.schema.student_stats import StudentStatsRequest,StudentStatsUpdateRequest, StudentStatsResponse
from app.database import get_db  

router = APIRouter(prefix="/student-stats", tags=["Student Stats"])

@router.post("/", response_model=StudentStatsResponse)
def create(stats: StudentStatsRequest, db: Session = Depends(get_db)):
    return crud.create_student_stats(db, stats)


@router.get("/{student_id}", response_model=StudentStatsResponse)
def read(student_id: int, db: Session = Depends(get_db)):
    stats = crud.get_student_stats(db, student_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return stats


@router.put("/{student_id}", response_model=StudentStatsResponse)
def update(student_id: int, stats: StudentStatsUpdateRequest, db: Session = Depends(get_db)):
    updated = crud.update_student_stats(db, student_id, stats)
    if not updated:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return updated


@router.delete("/{student_id}", response_model=StudentStatsResponse)
def delete(student_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student_stats(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student stats not found")
    return deleted
