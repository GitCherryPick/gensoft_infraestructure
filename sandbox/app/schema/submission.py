from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Submission(BaseModel):
    UserId: Optional[int] = None
    code: str
    taskId: int

class SubmissionBase(BaseModel):
    user_id: int
    code: str
    result: str

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionUpdate(BaseModel):
    code: Optional[str] = None
    result: Optional[str] = None

class SubmissionOut(SubmissionBase):
    submission_id: int
    submission_date: datetime

    class Config:
        from_attributes = True