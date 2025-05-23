from pydantic import BaseModel
from typing import Optional

class ExerciseBase(BaseModel):
    instructor_id: int 
    title: str
    prompt: str
    target_code: str
    visible_lines: str
    instructor_comment: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

# ExerciseUpdate

class ExerciseOut(BaseModel):
    id: int

    class Config:
        from_attributes = True
