from app.model.feedback_tasks import FeedbackTask
from app.schema.feedback_tasks import FeedbackTaskRequest, FeedbackTaskResponse, FeedbackTaskUpdate
from sqlalchemy.orm import Session

def create_feedback(db: Session, task: FeedbackTaskRequest):
    """
    Create a feedback task for a student.
    """
    new_feedback_task = FeedbackTask(
        student_id=task.student_id,
        task_id_lab=task.task_id_lab,
        task_id_rep=task.task_id_rep,
        feedback_ai=task.feedback_ai,
        feedback_docente=task.feedback_docente,
        n_intentos=task.n_intentos,
        estado=task.estado
    )
    db.add(new_feedback_task)
    db.commit()
    db.refresh(new_feedback_task)
    return new_feedback_task

def delete_feedback(db: Session, task_id: int):
    """
    Delete a feedback task by its ID.
    """
    feedback_task = db.query(FeedbackTask).filter(FeedbackTask.id == task_id).first()
    if not feedback_task:
        return None
    db.delete(feedback_task)
    db.commit()
    return feedback_task

def get_feedback_by_id(db: Session, feedback_id: int):
    """
    Get a feedback task by its ID.
    """
    return db.query(FeedbackTask).filter(FeedbackTask.id == feedback_id).first()

def update_feedback_by_id(db: Session, feedback_id: int, new_task: FeedbackTaskUpdate):
    """
    Update feedback task by its ID
    """
    feedback_task = get_feedback_by_id(db, feedback_id)
    if not feedback_task:
        return None
    for field, value in new_task.model_dump(exclude_unset=True).items():
        setattr(feedback_task, field, value)
    db.commit()
    db.refresh(feedback_task)
    return feedback_task
    
    