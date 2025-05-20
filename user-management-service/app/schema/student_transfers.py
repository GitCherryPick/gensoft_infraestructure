from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, Dict

class TypesStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"

class StudentTransferCreate(BaseModel):
    user_id: int
    from_institution: int
    to_institution: int
    transfer_date: Optional[datetime]
    progress_snapshot: Optional[Dict] 
    status: TypesStatus

class StudentTransferResponse(BaseModel):
    id: int
    user_id: int
    from_institution: int
    to_institution: int
    transfer_date: Optional[datetime]
    progress_snapshot: Optional[Dict] 
    status: TypesStatus
