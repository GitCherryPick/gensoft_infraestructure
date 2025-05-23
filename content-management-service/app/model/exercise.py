from sqlalchemy import Column, Integer, String, Text, JSON
from app.model.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    prompt = Column(Text, nullable=False)
    target_code = Column(Text, nullable=False)
    visible_lines = Column(JSON, nullable=False)
    instructor_comment = Column(Text, nullable=True)



 

