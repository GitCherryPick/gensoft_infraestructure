from sqlalchemy import Column, Integer, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base

class ExamResponse(Base):
    __tablename__ = "exam_responses"

    response_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.exam_id"), nullable=False, index=True)
    student_id = Column(Integer, nullable=False)
    question_responses = Column(JSON, nullable=False)
    total_score = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())