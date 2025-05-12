from fastapi import APIRouter
from app.core.api_ai import ask_ai as ask_ai_core
from app.schema.ai_question import AIQuestion, AIResponse

router = APIRouter()

@router.post("/ask", response_model=AIResponse)
def ask_ai(ai_question: AIQuestion):
    """
    Asking a question to an AI model.
    """
    response = ask_ai_core(ai_question.question)
    return response
