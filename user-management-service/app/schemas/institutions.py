from pydantic import BaseModel

class InstitutionCreate(BaseModel):
    name: str
    address: str | None = None
    contact_email: str | None = None
    website: str | None = None

class InstitutionResponse(BaseModel):
    id: int
    name: str
    address: str | None = None
    contact_email: str | None = None
    website: str | None = None