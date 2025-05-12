from app.schema.ai_question import AIQuestion, AIResponse
from google import genai
from google.genai import types
import os

api_key_gensoft = os.getenv('AI_API_KEY')

if not api_key_gensoft:
    raise ValueError("API key for AI is not set. Please set the 'AI_API_KEY' environment variable.")

def ask_ai(question_text: str):
    """
    Asking a question to an AI model.
    """
    try:
        client = genai.Client(api_key=api_key_gensoft)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question_text,
            config=types.GenerateContentConfig(
                max_output_tokens=150,
                temperature=0.5,
            ),
        )
        return {
            "answer":response.text,
            "status":"success",
        }
    except Exception as e:
        print(f"Error al llamar a la API-gemini: {e}")
        return {
            "answer":str(e),
            "status":"error",
        }