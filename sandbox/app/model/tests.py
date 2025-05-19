from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Tests(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id=Column(Integer, ForeignKey("tasks.id"), nullable=False)
    input = Column(String(100), nullable=False)
    output = Column(String(100), nullable=False)
    