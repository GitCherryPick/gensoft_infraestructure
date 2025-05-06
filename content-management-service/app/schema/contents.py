from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import re

class ContentCreate(BaseModel):
    module_id: int
    content_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None
    
    @validator('content_type')
    def validate_content_type(cls, v):
        valid_types = ["text", "pdf", "image", "video", "slide", "url"]
        if v not in valid_types:
            raise ValueError(f"Tipo de contenido no válido. Tipos válidos: {', '.join(valid_types)}")
        return v
    
    @validator('video_url')
    def validate_video_url(cls, v, values):
        if v is not None and values.get('content_type') in ['video', 'url']:
            if not re.match(r'^https?://', v):
                raise ValueError('La URL debe comenzar con http:// o https://')
        return v


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
        from_attributes = True


class ContentUpdate(BaseModel):
    content_type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    file_path: Optional[str] = None
    
    @validator('content_type')
    def validate_content_type(cls, v):
        if v is not None:
            valid_types = ["text", "pdf", "image", "video", "slide", "url"]
            if v not in valid_types:
                raise ValueError(f"Tipo de contenido no válido. Tipos válidos: {', '.join(valid_types)}")
        return v
    
    @validator('video_url')
    def validate_video_url(cls, v):
        if v is not None:
            if not re.match(r'^https?://', v):
                raise ValueError('La URL debe comenzar con http:// o https://')
        return v

class TextContentCreate(BaseModel):
    module_id: int
    content: str
    title: Optional[str] = None

class UrlContentCreate(BaseModel):
    module_id: int
    url: str
    title: Optional[str] = None
    
    @validator('url')
    def validate_url(cls, v):
        if not re.match(r'^https?://', v):
            raise ValueError('La URL debe comenzar con http:// o https://')
        return v
