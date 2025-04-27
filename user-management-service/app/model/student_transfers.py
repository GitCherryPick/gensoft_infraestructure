from datetime import datetime
from sqlalchemy import JSON, Column, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum

class TypesStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"

class StudentTransfer(Base):
    __tablename__ = "student_transfers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_institution = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    to_institution = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    transfer_date = Column(DateTime, default=datetime.utcnow)
    progress_snapshot = Column(JSON, nullable=True)
    status = Column(Enum(TypesStatus), nullable=False)

    user_rel = relationship("User", back_populates="student_transfer_rel")
    from_institution_rel = relationship("Institution", foreign_keys=[from_institution], backref="from_transfer_rel")
    to_institution_rel = relationship("Institution", foreign_keys=[to_institution], backref="to_transfer_rel")