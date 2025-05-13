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
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    enunciado: str

class TaskCreate(TaskBase):
    tests: Optional[List[TestCreate]] = []

class Task(TaskBase):
    id: int
    created_at: datetime
    tests: List[Test] = []

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: str
    enunciado: str