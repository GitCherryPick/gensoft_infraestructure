from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from .base import Base

class FeedbackTask(Base):
    __tablename__= 'feedback_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    task_id_lab = Column(Integer, nullable=True)
    task_id_rep = Column(Integer, nullable=True)
    feedback_ai = Column(JSON, nullable=True)
    feedback_docente = Column(JSON, nullable=True)
    n_intentos = Column(Integer, default=0, nullable=False)
    estado = Column(String, nullable=False, default='pendiente')  # 'pendiente', 'completado', 'fallido'