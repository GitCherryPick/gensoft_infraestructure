from fastapi import APIRouter, HTTPException
from app.core.ai_feedback import get_feedback_ai
from app.schema.replicator_prev import ResultReplicator

router = APIRouter()

@router.post("/ai-feedback/replicator")
async def ask_ai_feedback_replicator(request: ResultReplicator):
    """
    Asking a question for replicated code support.
    """
    response = await get_feedback_ai(request)
    if not response:
        raise HTTPException(status_code=418, detail="Bad connection with ai-ms")
    return response