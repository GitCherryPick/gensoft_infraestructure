from pydantic import BaseModel

class FeedbackTask(BaseModel):
    student_id: str
    task_id_lab: int = None
    task_id_rep: int = None
    feedback_ai: dict = None
    feedback_docente: dict = None
    n_intentos: int = 0
    estado: str = 'pendiente' 

    class Config:
        from_attributes = True 

class FeedbackTaskRequest(FeedbackTask):
    pass

class FeedbackTaskResponse(FeedbackTask):
    id: int

    class Config:
        from_attributes = True