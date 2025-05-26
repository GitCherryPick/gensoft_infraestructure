from fastapi import APIRouter, Depends, HTTPException
from app.model.feedback_tasks import FeedbackTask
from app.schema.feedback_tasks import FeedbackTaskRequest, FeedbackTaskResponse
from app.database import get_db
from app.services.feedback_task import create_feedback

router = APIRouter()

@router.post("/exercise", response_model=FeedbackTaskResponse)
def create_feedback_task(task: FeedbackTaskRequest, db=Depends(get_db)):
    response = create_feedback(db, task)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to create feedback task")
    return response