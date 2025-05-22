from pydantic import BaseModel
from typing import List, Optional

class ReplicatedFeedback(BaseModel):
    errores_sintacticos: List[str] = []
    estructura_igual_a_objetivo: bool = False
    puntaje_similitud: float
    diferencias_detectadas: List[str] = []
    pistas_generadas: List[str] = []

    class Config:
        from_attributes = True 

class LabFeedback(BaseModel):
    puntaje: int
    feedback: str
    estado: str
    pistas: Optional[List[str]] = []
    warnings: Optional[List[str]] = []
    errores: Optional[List[str]] = []
    
    class Config:
        from_attributes = True
        