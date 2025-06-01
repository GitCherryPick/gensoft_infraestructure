from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, func
from app.model.base import Base

class UsedHint(Base):
    __tablename__ = "used_hints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    hint_id = Column(Integer, ForeignKey("hints.hint_id"))
    used_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'task_id', 'hint_id', name='uq_user_task_hint'),
    )
