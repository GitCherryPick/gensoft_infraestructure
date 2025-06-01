# models/task.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DateTime
from .base import Base
from datetime import datetime

class CodeTask(Base):
    __tablename__ = 'code_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), index=True)
    description = Column(Text)
    expected_code = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True) 
    template_code = Column(Text, nullable=True)
    date_limit = Column(DateTime, nullable = True)
    grade = Column(Integer, nullable = True)
    created_at = Column(TIMESTAMP, default=datetime.now)
