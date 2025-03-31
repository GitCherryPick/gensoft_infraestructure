from pydantic import BaseModel

class InstitutionCreate(BaseModel):
    name: str
    address: str 
    contact_email: str 
    website: str 

class InstitutionResponse(BaseModel):
    id: int
    name: str
    address: str 
    contact_email: str 
    website: str 