from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.model.base import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    difficulty = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")
    help_resources = relationship("HelpResource", back_populates="course", cascade="all, delete-orphan")
    
    # reviews = relationship("Review", back_populates="course", cascade="all, delete-orphan")
