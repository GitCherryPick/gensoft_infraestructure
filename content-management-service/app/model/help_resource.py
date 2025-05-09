from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.model.base import Base

class HelpResource(Base):
    __tablename__ = "help_resources"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(150), nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)
    file_path = Column(String(255))
    video_url = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    course = relationship("Course", back_populates="help_resources")
