from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentBase(BaseModel):
    module_id: int
    content_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class ContentOut(ContentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True