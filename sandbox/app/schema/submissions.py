from pydantic import BaseModel
from datetime import datetime

class SubmissionCreate(BaseModel):
    user_id: int
    code: str

class SubmissionResponse(BaseModel):
    submission_id: int
    user_id: int
    code: str
    submission_date: datetime
    result: str