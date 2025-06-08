from fastapi import APIRouter, Depends, HTTPException
from app.model.feedback_tasks import FeedbackTask
from app.schema.feedback_tasks import FeedbackTaskRequest, FeedbackTaskResponse, FeedbackTaskUpdate
from app.database import get_db
from app.services.feedback_task import create_feedback, delete_feedback, get_feedback_by_id, update_feedback_by_id

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

@router.get("/exercise/{feedback_id}", response_model=FeedbackTaskResponse)
def get_feedback_task(feedback_id: int, db=Depends(get_db)):
    feedback_task = get_feedback_by_id(db, feedback_id)
    if not feedback_task:
        raise HTTPException(status_code=404, detail="Feedback task not found")
    return feedback_task

@router.put("/exercise/{feedback_id}", response_model=FeedbackTaskResponse)
def update_feedback_task(feedback_id: int, updated: FeedbackTaskUpdate, db=Depends(get_db)):
    feedback_task = update_feedback_by_id(db, feedback_id, updated)
    if not feedback_task:
        raise HTTPException(status_code=404, detail="Feedback task not found")
    return feedback_task