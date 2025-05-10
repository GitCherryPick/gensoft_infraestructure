from app.schema.ai_question import AIQuestion, AIResponse
#from google import genai
import google.generativeai as genai 
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('AI_API_KEY')

if not api_key:
    raise ValueError("API key for AI is not set. Please set the 'AI_API_KEY' environment variable.")

def ask_ai(question_text: str):
    """
    Asking a question to an AI model.
    """
    try:
        # client = genai.Client(api_key)
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash",
        #     contents=question.question,
        # )
        # return {
        #     "answer":response.text,
        #     "status":"success",
        # }
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(question_text)
        if response.parts:
            answer_text = response.text
            status_text = "success"
        else:
            block_reason = "Unknown"
            if response.prompt_feedback and hasattr(response.prompt_feedback, 'block_reason'):
                block_reason = response.prompt_feedback.block_reason.name if response.prompt_feedback.block_reason else "Unknown no se"
                answer_text = f"NO se pudo generar la respuesta. Block reason: {block_reason}"
                status_text = "error"
        return {
            "answer": answer_text,
            "status": status_text,
        }
    except Exception as e:
        print(f"Error al llamar a la API-gemini: {e}")
        return {
            "answer":str(e),
            "status":"error",
        }