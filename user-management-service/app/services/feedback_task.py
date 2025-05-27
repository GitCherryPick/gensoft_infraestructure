from app.model.feedback_tasks import FeedbackTask
from app.schema.feedback_tasks import FeedbackTaskRequest, FeedbackTaskResponse
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