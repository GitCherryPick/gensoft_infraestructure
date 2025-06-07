from sqlalchemy import Column, Enum, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)  ##duda unique
    description = Column(String(255), nullable=True)
    
    user_roles_rel = relationship("UserRoles", back_populates="role_rel")