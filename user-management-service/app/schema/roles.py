import enum
from pydantic import BaseModel, constr
from typing import Optional, List

class TypeRole(enum.Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"

class RoleBase(BaseModel):
    name: TypeRole
    description: Optional[constr(max_length=255)] 
   
class RoleResponse(RoleBase):
    id: int