from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class QuestionResponse(BaseModel):
    question_id: int
    answer: Optional[str] = None
    answers: Optional[List[str]] = None
    code_solution: Optional[str] = None
    is_correct: Optional[bool] = None
    points_earned: Optional[float] = None

class ExamResponseBase(BaseModel):
    exam_id: int
    student_id: int
    question_responses: List[QuestionResponse]
    total_score: Optional[float] = None

class ExamResponseCreate(ExamResponseBase):
    pass

class ExamResponseOut(ExamResponseBase):
    response_id: int
    created_at: datetime

    class Config:
        from_attributes = True 