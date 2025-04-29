from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentCreate(BaseModel):
    module_id: int
    content_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None


class ContentOut(BaseModel):
    id: int
    module_id: int
    content_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True



class ContentUpdate(BaseModel):
    content_type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None
