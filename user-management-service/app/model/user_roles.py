from datetime import datetime
from sqlalchemy import JSON, Column, ForeignKey, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    user_rel = relationship("User", backref="user_with_rol_rel")
    role_rel = relationship("Role", back_populates="user_roles_rel")