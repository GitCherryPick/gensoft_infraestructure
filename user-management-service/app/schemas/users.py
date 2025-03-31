from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    status: str
    created_at: str
    updated_at: str
    last_login: str | None = None