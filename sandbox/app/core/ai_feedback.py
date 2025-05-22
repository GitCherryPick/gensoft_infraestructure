import httpx

AI_ASSISTANT_URL = "http://localhost:8005/ai/ask"

async def get_feedback_ai(content: str):
    """
    Get feedback for replicated code from AI assistant.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(AI_ASSISTANT_URL, json={"question": content})
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": "Failed to get feedback from AI assistant."}