from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from app.model.submissions import Submission
from app.schema.submission import SubmissionCreate, SubmissionUpdate, SubmissionOut

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def create_submission(sub: SubmissionCreate, db: Session = Depends(get_db)):

    if sub.tipo_problema not in ("task", "code_task"):
        raise HTTPException(
            status_code=400, detail="tipo_problema debe ser 'task' o 'code_task'"
        )

    db_sub = Submission(**sub.dict())

    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.get("/", response_model=List[SubmissionOut])
def get_submissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Submission).offset(skip).limit(limit).all()

@router.get("/{submission_id}", response_model=SubmissionOut)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    db_sub = db.query(Submission).filter(Submission.submission_id == submission_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return db_sub

@router.put("/{submission_id}", response_model=SubmissionOut)
def update_submission(submission_id: int, sub_update: SubmissionUpdate, db: Session = Depends(get_db)):
    db_sub = db.query(Submission).get(submission_id)
    if not db_sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    update_data = sub_update.dict(exclude_unset=True)

    if "tipo_problema" in update_data and update_data["tipo_problema"] not in ("task", "code_task"):
        raise HTTPException(
            status_code=400, detail="tipo_problema debe ser 'task' o 'code_task'"
        )

    for field, value in update_data.items():
        setattr(db_sub, field, value)

    db.commit()
    db.refresh(db_sub)
    return db_sub

@router.delete("/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    db_sub = db.query(Submission).get(submission_id)
    if not db_sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    db.delete(db_sub)
    db.commit()
    return None
