from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Option(BaseModel):
    option_id: int
    text: str

class TestCase(BaseModel):
    description: str
    expected_output: str
    test_case_id: int
    input: str
    is_visible: bool
    name: str
    points: int  

class Question(BaseModel):
    question_id: int
    title: str
    description: str
    points: int
    type: str
    options: Optional[List[Option]] = None
    correct_answer: Optional[str] = None
    correct_answers: Optional[List[str]] = None
    target_code: Optional[str] = None
    visible_lines: Optional[List[int]] = None
    test_cases: Optional[List[TestCase]] = None

class ExamBase(BaseModel):
    title: str
    description: str
    time_limit: int
    questions: List[Question]
    settings: Dict

class ExamCreate(ExamBase):
    pass

class ExamOut(ExamBase): 
    exam_id: int
    created_at: datetime

    class config:
        from_attributes=True


        