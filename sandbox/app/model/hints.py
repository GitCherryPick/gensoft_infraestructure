from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.model.base import Base

class Hints(Base):
    __tablename__ = "hints"

    hint_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True) 
    hint_order = Column(Integer, nullable = False)
    hint_text = Column(Text, nullable=False)
    penalty_points = Column(Float, default=0, nullable=False)