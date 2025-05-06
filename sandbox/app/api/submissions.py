from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.submissions import Submission
from app.schema.submissions import SubmissionCreate, SubmissionResponse
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/submissions/", response_model=SubmissionResponse)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    new_submission = submission(
        user_id=submission.user_id,
        code=submission.code,
        result="pending",
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission