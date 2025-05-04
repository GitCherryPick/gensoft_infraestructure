from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.model.base import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    level = Column(String(20))
    module_order = Column(Integer)

    course = relationship("Course", back_populates="modules")
    contents = relationship("Content", back_populates="module", cascade="all, delete-orphan")
    
    # institution = relationship("Institution", back_populates="modules")
