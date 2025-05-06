from pydantic import BaseModel
from typing import Optional

class ModuleBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    level: str
    module_order: Optional[int] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    module_order: Optional[int] = None
    course_id: Optional[int] = None

class Module(ModuleBase):
    id: int

    class Config:
        from_attributes = True 
