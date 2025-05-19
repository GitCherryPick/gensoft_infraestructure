from pydantic import BaseModel

class SuggestionBase(BaseModel):
    student_id: int

class SuggestionCreate(SuggestionBase):
    suggestion_text: str

class SuggestionUpdate(SuggestionBase):
    suggestion_text: str
    is_accepted: bool

class SuggestionOut(SuggestionBase):
    id: int
    suggestion_text: str
    is_accepted: bool

    class Config:
        from_attributes = True