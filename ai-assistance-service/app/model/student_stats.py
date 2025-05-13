from datetime import datetime
from sqlalchemy import JSON, Column, Integer, DateTime
from .base import Base

class StudentStats(Base):
    __tablename__ = "student_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, unique=True,nullable=False)
    total_activities_answered = Column(Integer, default=0)
    common_mistakes = Column(JSON)
    interests = Column(JSON)
    performance_stats = Column(JSON)
    last_accessed = Column(DateTime, default=datetime.utcnow)