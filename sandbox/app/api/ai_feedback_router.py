from fastapi import APIRouter, HTTPException
from app.core.ai_feedback import get_feedback_ai, get_pruebita, get_feedback_ai_lab
from app.schema.replicator_prev import ResultReplicator, ReplicatedFeedback
from app.schema.lab_prev import LabFeedback, LabRequest

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

@router.post("/ai-feedback/lab", response_model=LabFeedback)
async def ask_ai_feedback_labs(request: LabRequest):
    """
    Asking a question for lab code support.
    """
    response = await get_feedback_ai_lab(request)
    if not response:
        raise HTTPException(status_code=418, detail="Bad connection with ai-ms")
    
    if isinstance(response, str):
        import json
        response = json.loads(response)
    return LabFeedback(**response)