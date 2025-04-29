from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HelpResourceBase(BaseModel):
    title: str
    resource_type: str
    description: Optional[str] = None
    file_path: Optional[str] = None
    video_url: Optional[str] = None

class HelpResourceCreate(HelpResourceBase):
    course_id: Optional[int]

class HelpResourceUpdate(HelpResourceBase):
    pass

class HelpResourceOut(HelpResourceBase):
    id: int
    course_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
