from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

class HelpResource(HelpResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True