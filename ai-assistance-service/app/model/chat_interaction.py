from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Text
from .base import Base

class ChatInteraction(Base):
    __tablename__ = "chat_interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    message_from_chat = Column(Text)
    message_from_user = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)