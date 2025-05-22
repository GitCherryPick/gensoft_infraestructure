from fastapi import HTTPException
import httpx
from app.schema.replicator_prev import ResultReplicator

AI_ASSISTANT_URL = "http://localhost:8005/ai"

async def get_feedback_ai(content: ResultReplicator):
    """
    Get feedback for replicated code from AI assistant.
    """
    prompt = f"""
    Eres un evaluador de código python, tu tarea es analizar el código proporcionado por el estudiante: {content.codigo_estudiante} y compararlo con
    el código de referencia: {content.codigo_objetivo}. Dado el contexto del ejercicio: {content.contexto_ejercicio} y las consignas del docente: 
    {content.consignas_docente}, para los campos resultantes considera:
    *   "puntaje_similitud": Un número de punto flotante entre 0 y 10 que representa la similitud del código del estudiante con el código objetivo. La puntuación se calcula de la siguiente manera:
        -0.5 puntos si las variables están mal escritas.
        -1 punto por errores de indentación o nombres clave incorrectos (como for o while).
        -10 puntos si no hay contenido en el código del estudiante.
        -2 puntos si no se cumple alguna de las consignas.
    *   "diferencias_detectadas": Una lista de descripciones técnicas de las diferencias entre el código del estudiante y el código objetivo, pensada para el docente.
    *   "pistas_generadas": Una lista de pistas para el estudiante, que explican las diferencias de manera más sencilla y amigable.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_ASSISTANT_URL}/ask-feedback/replicator",
                json={"ai_question": prompt}
            )
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to AI Assistant at {AI_ASSISTANT_URL}"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to AI Assistant timed out"
        )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI Assistant service error: {str(e)}"
        )