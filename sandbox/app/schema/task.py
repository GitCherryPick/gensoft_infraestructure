from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestBase(BaseModel):
    input: str
    output: str
    
    class Config:
        from_attributes = True

class TestCreate(TestBase):
    pass

class Test(TestBase):
    id: int
    task_id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    enunciado: str

class TaskOptionalFields(BaseModel):
    pistas: Optional[List[str]] = []
    date_limit: Optional[datetime] = None
    grade: Optional[int] = 0
    status: Optional[str] = "Abierta"
    id_docente: Optional[int] = 0
    codigo_plantilla: Optional[str] = ""
    lineas_visibles: Optional[List[int]] = []
    lines_blocked: Optional[List[int]] = []

class TaskCreate(TaskBase, TaskOptionalFields):
    tests: Optional[List[TestCreate]] = []

class TaskOut(TaskBase, TaskOptionalFields):
    id: int
    created_at: datetime
    tests: List[Test] = []

    class Config:
        from_attributes = True

class TaskUpdate(TaskBase, TaskOptionalFields):
    pass