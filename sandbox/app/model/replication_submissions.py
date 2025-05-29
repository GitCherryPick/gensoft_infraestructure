from sqlalchemy import Column, Integer, Text, DateTime, Boolean, Float
from sqlalchemy.sql import func
from app.model.base import Base

class ReplicationSubmission(Base):
    __tablename__ = "replication_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    exercise_id = Column(Integer, nullable=False, index=True)
    student_code = Column(Text, nullable=False)
    submission_date = Column(DateTime(timezone=True), server_default=func.now())
    typing_duration_seconds = Column(Integer, nullable=False)
    errores_sintacticos = Column(Text, nullable=False, default='[]')  # JSON serializado
    ejecucion_simulada_exitosa = Column(Boolean, nullable=False, default=False)
    estructura_igual_a_objetivo = Column(Boolean, nullable=False, default=False)
    puntaje_similitud = Column(Float, nullable=False, default=0.0)
    diferencias_detectadas = Column(Text, nullable=False, default='[]')  # JSON serializado
    pistas_generadas = Column(Text, nullable=False, default='[]')  # JSON serializado
    is_passed = Column(Boolean, nullable=False, default=False)
