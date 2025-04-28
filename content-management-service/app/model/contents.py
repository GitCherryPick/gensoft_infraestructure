from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Content(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    content_type = Column(String(20), nullable=False)
    title = Column(String(150), nullable=True)
    content = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=True)
    file_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación opcional si quieres acceder desde Content al módulo
    module = relationship("Module", back_populates="contents")
