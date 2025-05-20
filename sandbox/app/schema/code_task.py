from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str 
    expected_code: Optional[str] = None
    expected_result: Optional[str] = None
    template_code: Optional[str] = None

class TaskRequest(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class StudentReply(BaseModel):
    task_replicator_id: int
    student_code: str