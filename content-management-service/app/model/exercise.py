from sqlalchemy import Column, Integer, String, Text
from app.model.base import Base
import json

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    prompt = Column(Text, nullable=False)
    target_code = Column(Text, nullable=False)
    visible_lines = Column(Text, nullable=False)
    instructor_comment = Column(Text, nullable=True)

 

