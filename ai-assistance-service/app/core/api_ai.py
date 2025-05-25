from typing import Dict
from app.schema.ai_question import AIQuestion, AIResponse
from google import genai
from google.genai import types
import os
from typing import Union
from app.schema.ai_feedback import ReplicatedFeedback, LabFeedback

chat_sessions: Dict[str, any] = {}
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
def ask_ai_feedback_rep(question_text: str):
    """
    Asking a question to an AI model.
    """
    client = genai.Client(api_key=api_key_gensoft)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question_text,
        config={
            "response_mime_type": "application/json",
            "response_schema": ReplicatedFeedback
        }
    )
    return response.text
    
def ask_ai_feedback_lab(question_text: str):
    """
    Asking a question to an AI model about analysing code
    """
    client = genai.Client(api_key=api_key_gensoft)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question_text,
        config={
            "response_mime_type": "application/json",
            "response_schema": LabFeedback
        }
    )
    return response.text

def conversate_ai(user_id: int, question_text: str):
    """
    Conversing with an AI model.
    """
    try:
        if user_id not in chat_sessions:
            client = genai.Client(api_key=api_key_gensoft)
            chat = client.chats.create(
                model="gemini-2.0-flash",
            )
            chat_sessions[user_id] = chat
        else:
            chat = chat_sessions[user_id]

        response = chat.send_message_stream(question_text)
        message_show = ""
        for chunk in response:
            if chunk.text:
                message_show += chunk.text
            
        return {
            "status": "success",
            "question": question_text,
            "answer": message_show
        }
    except Exception as e:
        print(f"Error al llamar a la API-gemini: {e}")
        return {
            "status": "error",
            "question": "Fallido",
            "answer": f"Error {e}"
        }
