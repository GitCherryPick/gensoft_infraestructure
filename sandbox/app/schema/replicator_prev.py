from typing import List
from pydantic import BaseModel

class ResultReplicator(BaseModel):
    codigo_estudiante: str
    codigo_objetivo: str
    consignas_docente: str
    contexto_ejercicio: str

    class Config:
        from_attributes = True

class ReplicatedFeedback(BaseModel):
    errores_sintacticos: List[str]
    estructura_igual_a_objetivo: bool 
    puntaje_similitud: float
    diferencias_detectadas: List[str] 
    pistas_generadas: List[str] 

    class Config:
        from_attributes = True 