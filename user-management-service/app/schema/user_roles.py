from pydantic import BaseModel, constr
from datetime import datetime

class UserRolesCreate(BaseModel):
    user_id: int
    role_id: int

class UserRolesResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    created_date: datetime