from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class TypeDifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), index=True, nullable=False)
    description = Column(nullable=True)
    difficulty_level = Column(Enum(TypeDifficultyLevel))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime,  default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    students_rel = relationship("Student", backref="course_student_rel")
    module_course_rel = relationship("Module", back_populates="course_module_rel")