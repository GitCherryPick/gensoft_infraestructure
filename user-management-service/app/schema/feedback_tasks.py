from typing import List
from pydantic import BaseModel

class FeedbackTask(BaseModel):
    student_id: int
    task_id_lab: int = 0
    task_id_rep: int = 0
    feedback_ai: List[str] = []
    feedback_docente: List[str] = []
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