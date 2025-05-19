from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class GradeBase(BaseModel):
    user_id: int
    score: int = Field(..., ge=0, le=100)

class GradeCreate(GradeBase):
    pass

class GradeUpdate(BaseModel):
    score: Optional[int] = Field(None, ge=0, le=100)

class GradeOut(GradeBase):
    grade_id: int
    is_passed: bool
    grade_date: datetime

    class Config:
        from_attributes = True