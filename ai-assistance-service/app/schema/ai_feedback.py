from pydantic import BaseModel
from typing import List, Optional

class ReplicatedFeedback(BaseModel):
    errores_sintacticos: List[str]
    estructura_igual_a_objetivo: bool 
    puntaje_similitud: float
    diferencias_detectadas: List[str] 
    pistas_generadas: List[str] 

    class Config:
        from_attributes = True 

class ErrorFeedback(BaseModel):
    error: str
    line: int

    class Config:
        from_attributes = True

class LabFeedback(BaseModel):
    feedback: str
    estado: str
    warnings: Optional[List[str]]
    errores: Optional[ErrorFeedback]
    
    class Config:
        from_attributes = True
        