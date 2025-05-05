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

class ModuleUpdate(ModuleBase):
    pass

class Module(ModuleBase):
    id: int

    class Config:
        orm_mode = True