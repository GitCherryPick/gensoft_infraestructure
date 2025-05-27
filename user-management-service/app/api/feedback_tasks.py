from fastapi import APIRouter, Depends, HTTPException
from app.model.feedback_tasks import FeedbackTask
from app.schema.feedback_tasks import FeedbackTaskRequest, FeedbackTaskResponse
from app.database import get_db
from app.services.feedback_task import create_feedback, delete_feedback

router = APIRouter()

@router.post("/exercise", response_model=FeedbackTaskResponse)
def create_feedback_task(task: FeedbackTaskRequest, db=Depends(get_db)):
    response = create_feedback(db, task)
    if not response:
        raise HTTPException(status_code=500, detail="Failed to create feedback task")
    return response

@router.delete("/exercise/{task_id}", response_model=FeedbackTaskResponse)
def delete_feedback_task(task_id: int, db=Depends(get_db)):
    response = delete_feedback(db, task_id)
    if not response:
        raise HTTPException(status_code=404, detail="Feedback task not found")
    return response