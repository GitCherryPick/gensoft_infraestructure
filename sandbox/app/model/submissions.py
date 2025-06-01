from sqlalchemy import JSON, Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.model.base import Base

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    code = Column(Text, nullable=False)
    submission_date = Column(DateTime(timezone=True), server_default=func.now())
    result = Column(String(255), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True) 
    code_task_id = Column(Integer, ForeignKey("code_tasks.id"), nullable=True)
    tipo_problema = Column(String(50), nullable=False) # 'task' o 'code_task'
    score = Column(Integer, nullable=True)  # ✅ Nuevo campo de puntaje
    test_feedback = Column(JSON, nullable=True)
    status = Column(String(12), nullable=False, default='Sin revisar')