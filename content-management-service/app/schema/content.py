from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

class Content(ContentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True