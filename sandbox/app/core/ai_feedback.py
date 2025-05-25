from fastapi import HTTPException
import httpx
from app.schema.replicator_prev import ResultReplicator
from app.schema.lab_prev import LabRequest

AI_ASSISTANT_URL = "http://ai-assistance-service:8005"

async def get_feedback_ai(content: ResultReplicator):
    """
    Get feedback for replicated code from AI assistant.
    """
    prompt = f"""
    Eres un evaluador de código python, tu tarea es analizar el código proporcionado por el estudiante: {content.codigo_estudiante} y compararlo con
    el código de referencia: {content.codigo_objetivo}. Dado el contexto del ejercicio: {content.contexto_ejercicio} y las consignas del docente: 
    {content.consignas_docente}, para los campos resultantes considera:
    *   "errores_sintacticos": Una lista de errores sintácticos encontrados en {content.codigo_estudiante} basicamente si no se escribe correctamente palabras reservadas de python y tambien si
    no existe una indentacion correcta cuenta eso por favor.
    *   "estructura_igual_a_objetivo": Un booleano que indica si la estructura del código del estudiante es igual a la del código objetivo.
    *   "puntaje_similitud": Un número de punto flotante entre 0 y 10 que representa la similitud del código del estudiante con el código objetivo. La puntuación se calcula de la siguiente manera:
        -0.5 puntos por cada variable mal escrita.
        -1.5 punto por errores de indentación o nombres clave incorrectos (como for o while).
        -10 puntos si no hay contenido en el código del estudiante.
        -2.5 puntos por cada consigna sin cumplir.
    *   "diferencias_detectadas": Una lista de descripciones técnicas de las diferencias entre el código del estudiante y el código objetivo, pensada para el docente.
    *   "pistas_generadas": Una lista de pistas para el estudiante, que explican las diferencias de manera más sencilla y amigable.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_ASSISTANT_URL}/ai/ask-feedback/replicator",
                json={"question": prompt}
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
    
async def get_pruebita():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{AI_ASSISTANT_URL}/"
            )
            return resp.json()
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to AI Assistant at {AI_ASSISTANT_URL}/"
        )
    
async def get_feedback_ai_lab(content: LabRequest):
    """
    Get feedback for lab code from AI assistant.
    """
    prompt = f"""
    Eres un evaluador de código python, tu tarea es analizar el código proporcionado por el estudiante: {content.codigo_estudiante}. Dado el contexto del ejercicio: 
    {content.enunciado} y los errores encontrados en el resultado(si es que existen): {content.resultado_obtenido}, para los campos resultantes considera:
    *   "feedback_docente": Una lista de descripciones técnicas de los errores o warnings del código del estudiante, pensada para el docente. 
    *   "warnings": Por favor, si hay warnings en el código del estudiante, indícalos aquí en la forma solicitada.
    *   "pistas_generadas": Solo necesito encontrar dos tipos de errores, tambien menciona la linea principal de ambos:
        -Si content.resultado_obtenido contiene  las palabras"Timeout", entonces el error es RuntimeError busca la condicion que podria provocarlo para la linea.
        -Si content.resultado_obtenido contiene un resultado sin errores ni ":", entonces verifica si el codigo del estudiante tiene variables sin usar, llama al
        error "UnusedVariable" y dime la primera linea de variable sin usar.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_ASSISTANT_URL}/ai/ask-feedback/lab",
                json={"question": prompt}
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
    