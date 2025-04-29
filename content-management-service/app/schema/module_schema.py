from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ModuleBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    module_order: Optional[int] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(ModuleBase):
    pass

class ModuleOut(ModuleBase):
    id: int

    class Config:
        orm_mode = True