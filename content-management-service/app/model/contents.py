from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    content_type = Column(String(20), nullable=False)
    title = Column(String(150))
    content = Column(Text)
    video_url = Column(String(255))
    file_path = Column(String(255))
    created_at = Column(TIMESTAMP)

    module = relationship("Module", back_populates="contents")
