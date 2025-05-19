from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Grade(Base):
    __tablename__ = "grades"

    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    is_passed = Column(Boolean, nullable=False) 
    score = Column(Integer, nullable=False)
    grade_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_rel = relationship("User", back_populates="grade_rel")

    # Constraints
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="score_range"),
    )