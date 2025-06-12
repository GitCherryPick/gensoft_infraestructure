from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.model.base import Base

class Exam(Base):
    __tablename__ = "exams"

    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    time_limit = Column(Integer, nullable=False)
    questions = Column(JSON, nullable=False)
    settings = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now()) 

    exam_responses = relationship("ExamResponse", backref="exam_rel", cascade="all, delete-orphan")
