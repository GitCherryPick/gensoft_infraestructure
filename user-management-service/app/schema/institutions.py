from pydantic import BaseModel
from typing import Optional

class InstitutionCreate(BaseModel):
    name: str
    address: Optional[str] 
    contact_email: Optional[str] 
    website: Optional[str] 

class InstitutionResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] 
    contact_email: Optional[str] 
    website: Optional[str] 