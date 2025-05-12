from pydantic import BaseModel

class AIQuestion(BaseModel):
    question: str

class AIResponse(BaseModel):
    answer: str
    status: str

class AIConversateResponse(BaseModel):
    status: str
    question: str
    answer: str 