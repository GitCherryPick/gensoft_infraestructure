from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.api_ai import ask_ai as ask_ai_core
from app.core.api_ai import conversate_ai as conversate_ai_core 
from app.schema.ai_question import AIQuestion, AIResponse, AIConversateResponse
from app.schema.chat_interaction import ChatInput, ChatOutput
from app.model.chat_interaction import ChatInteraction
from app.database import get_db
from app.db.chat_db import save_important_message
router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(ai_question: AIQuestion):
    """
    Asking a question to an AI model.
    """
    response = ask_ai_core(ai_question.question)
    return response

@router.get("/saved/{user_id}", response_model=list[ChatOutput])
def get_saved(user_id: str, db: Session = Depends(get_db)):
    return db.query(ChatInteraction).filter(ChatInteraction.student_id == user_id).all()

@router.post("/chat", response_model=AIConversateResponse)
def chat(input_data: ChatInput, db: Session = Depends(get_db)):
    """
    Save the chat interaction to the database.
    """
    response = conversate_ai_core(input_data.user_id, input_data.question_text)
    if input_data.important and response["status"] == "success":
        save_important_message(
            db=db,
            user_id=input_data.user_id,
            content=response["answer"],
            question=response["question"],
        )
    
    return response