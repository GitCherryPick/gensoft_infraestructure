from datetime import datetime
from pydantic import BaseModel

class SavedMessage(BaseModel):
    student_id: int 
    message_from_chat: str 
    message_from_user: str
   
class ChatInput(BaseModel):
    user_id: int
    question_text: str
    important: bool = False

class ChatOutput(BaseModel):
    id: int
    student_id: int
    message_from_chat: str
    message_from_user: str
    timestamp: datetime