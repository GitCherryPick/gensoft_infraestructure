from pydantic import BaseModel
from typing import Optional, List

class ExerciseBase(BaseModel):
    instructor_id: int 
    title: str
    prompt: str
    target_code: str
    visible_lines: List[int]
    instructor_comment: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

# ExerciseUpdate

class ExerciseOut(ExerciseBase):
    exercise_id: int

    class Config:
        from_attributes = True
