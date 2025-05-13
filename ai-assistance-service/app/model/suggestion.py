from sqlalchemy import Boolean, Column, Integer, Text
from .base import Base

class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    suggestion_text = Column(Text, nullable=False)
    is_accepted = Column(Boolean, default=False)