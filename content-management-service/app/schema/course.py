from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True