from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestBase(BaseModel):
    input: str
    output: str

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

class TaskCreate(TaskBase):
    tests: Optional[List[TestCreate]] = []
    pistas: Optional[List[str]] = []
    date_limit: Optional[datetime] = None
    grade: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    tests: List[Test] = []
    pistas: Optional[List[str]] = []
    date_limit: Optional[datetime] = None
    grade: Optional[int] = None

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str
    enunciado: str
    pistas: Optional[List[str]] = []
    date_limit: Optional[datetime] = None
    grade: Optional[int] = None