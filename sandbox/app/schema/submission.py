from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestVeredict(BaseModel):
    veredict: str
    error: str = ""
    input: str
    expectedOutput: str
    output: str

class Submission(BaseModel):
    user_id: Optional[int] = None
    code: str
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str
    score: Optional[int] = None

class SubmissionBase(BaseModel):
    user_id: int
    code: str
    result: str
    status: Optional[str] = "Sin revisar"

class SubmissionInput(BaseModel):
    UserId: int
    code: str
    taskId: int

class SubmissionCreate(SubmissionBase):
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str
    test_feedback: Optional[List[TestVeredict]] = []

class SubmissionUpdate(BaseModel):
    code: Optional[str] = None
    result: Optional[str] = None
    score: Optional[int] = None
    test_feedback: Optional[List[TestVeredict]] = []
    status: Optional[str] = "Sin revisar"

class SubmissionOut(SubmissionBase):
    submission_id: int
    submission_date: datetime
    task_id: Optional[int] = None
    code_task_id: Optional[int] = None
    tipo_problema: str
    score: Optional[int] = None
    test_feedback: Optional[List[TestVeredict]] = []

class SubmissionResponse(SubmissionOut):
    username: str

    class Config:
        from_attributes = True
