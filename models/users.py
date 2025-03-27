from flask import session
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .institutions import Institution

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    last_login = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    student_transfer_rel = relationship("StudentTransfer", back_populates="user_rel")