from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Institution(Base):
    __tablename__ = "institutions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=True)
    contact_email = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)