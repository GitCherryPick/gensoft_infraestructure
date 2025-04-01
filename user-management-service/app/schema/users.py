from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str 

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    last_login: str