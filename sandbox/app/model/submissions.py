from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from app.model.base import Base

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    # exercise_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    code = Column(Text, nullable=False)
    submission_date = Column(DateTime(timezone=True), server_default=func.now())
    result = Column(String(255), nullable=False)
    