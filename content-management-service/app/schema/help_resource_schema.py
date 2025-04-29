from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HelpResourceBase(BaseModel):
    course_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    resource_type: str
    file_path: Optional[str] = None
    video_url: Optional[str] = None

class HelpResourceCreate(HelpResourceBase):
    pass

class HelpResourceUpdate(HelpResourceBase):
    pass

class HelpResourceOut(HelpResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True