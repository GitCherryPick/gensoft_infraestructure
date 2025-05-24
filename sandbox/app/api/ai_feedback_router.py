from fastapi import APIRouter, HTTPException
from app.core.ai_feedback import get_feedback_ai, get_pruebita
from app.schema.replicator_prev import ResultReplicator, ReplicatedFeedback

router = APIRouter()

@router.post("/ai-feedback/replicator", response_model=ReplicatedFeedback) 
async def ask_ai_feedback_replicator(request: ResultReplicator):
    """
    Asking a question for replicated code support.
    """
    response = await get_feedback_ai(request)
    if not response:
        raise HTTPException(status_code=418, detail="Bad connection with ai-ms")
    
    if isinstance(response, str):
        import json
        response = json.loads(response)
    return ReplicatedFeedback(**response)

@router.get("/ai-feedback/test")
async def ask_test():
    resp = await get_pruebita()
    if not resp:
        raise HTTPException(status_code=418, detail="Bad connection with ai-ms")
    return resp