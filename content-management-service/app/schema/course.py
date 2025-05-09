from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None

class CourseOut(CourseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat() if dt else None
        }
