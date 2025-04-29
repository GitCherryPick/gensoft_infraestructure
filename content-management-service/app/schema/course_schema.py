from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    modules: List[dict] = []
    help_resources: List[dict] = []
    reviews: List[dict] = []

    class Config:
        orm_mode = True