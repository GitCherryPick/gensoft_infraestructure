from pydantic import BaseModel
from typing import Optional
class Submission(BaseModel):
    UserId: Optional[int] = None
    code: str
    taskId: int
from datetime import datetime
from typing import Optional

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
        orm_mode = True
