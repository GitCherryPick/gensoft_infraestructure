from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.services.submissions_user import get_usernames_batch, generate_missing_submissions

from ..database import get_db
from app.model.submissions import Submission
from app.schema.submission import SubmissionCreate, SubmissionUpdate, SubmissionOut, SubmissionResponse

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def create_submission(sub: SubmissionCreate, db: Session = Depends(get_db)):

    if sub.tipo_problema not in ("task", "code_task"):
        raise HTTPException(
            status_code=400, detail="tipo_problema debe ser 'task' o 'code_task'"
        )

    db_sub = Submission(**sub.model_dump())

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

@router.get("/task/{task_id}", response_model=List[SubmissionResponse])
async def get_submission_by_task_id(task_id: int, db: Session = Depends(get_db)):
    db_subs = db.query(Submission).filter(Submission.task_id == task_id).all()

    if not db_subs:
        raise HTTPException(status_code=404, detail="Submissions not found")
    
    user_ids = list(set(sub.user_id for sub in db_subs))
    user_data_map = await get_usernames_batch(user_ids=user_ids)

    for sub in db_subs:
        sub.username = user_data_map.get(sub.user_id, "No identificado")
    return db_subs

@router.get("/task/{task_id}/{user_id}", response_model=List[SubmissionResponse])
async def get_submission_by_task_id(task_id: int, user_id: int, db: Session = Depends(get_db)):
    db_subs = db.query(Submission).filter(
        (Submission.task_id == task_id) & (Submission.user_id == user_id)
    ).order_by(Submission.submission_date.desc()).all()
    if not db_subs:
        raise HTTPException(status_code=404, detail="Submissions not found")
    
    user_ids = list(set(sub.user_id for sub in db_subs))
    user_data_map = await get_usernames_batch(user_ids=user_ids)
    for sub in db_subs:
        sub.username = user_data_map.get(sub.user_id, "No identificado")
    return db_subs

@router.post("/task/{task_id}/generate-missing-submissions")
async def generate_missing(task_id: int, db: Session = Depends(get_db)):
    return await generate_missing_submissions(task_id,db)

