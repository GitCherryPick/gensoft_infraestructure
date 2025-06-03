from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Submission(BaseModel):
    user_id: Optional[int] = None
    code: str
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str
    score: Optional[float] = None

class SubmissionBase(BaseModel):
    user_id: int
    code: str
    result: str

class SubmissionInput(BaseModel):
    UserId: int
    code: str
    taskId: int

class SubmissionCreate(SubmissionBase):
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str

class SubmissionUpdate(BaseModel):
    code: Optional[str] = None
    result: Optional[str] = None
    score: Optional[float] = None

class SubmissionOut(SubmissionBase):
    submission_id: int
    submission_date: datetime
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str
    score: Optional[float] = None

    class Config:
        from_attributes = True
