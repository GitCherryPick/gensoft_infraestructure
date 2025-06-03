from sqlalchemy import JSON, Column, Integer, String, Text, DateTime, ForeignKey, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
from app.model.base import Base 

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement = True)
    title = Column(String(30), unique = True, nullable = False)
    enunciado = Column(String(255), unique = True, nullable = False)
    pistas =  Column(JSON, nullable = True)
    date_limit = Column(DateTime, nullable = True)
    grade = Column(Integer, nullable = True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    status = Column(String(7), default="Abierta")

    tests = relationship("Tests", backref="task", cascade="all, delete-orphan")
