from datetime import datetime
from pydantic import BaseModel, constr
from typing import Optional, List

class UserCreate(BaseModel):
    username: constr(max_length=50)
    email: str
    password: str
    full_name: Optional[str]
    role: Optional[str]

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]