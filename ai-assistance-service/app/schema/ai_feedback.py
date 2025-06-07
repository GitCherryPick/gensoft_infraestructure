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
    line: str

    class Config:
        from_attributes = True

class LabFeedback(BaseModel):
    feedback_docente: str
    warnings: Optional[List[str]]
    errores: Optional[ErrorFeedback]
    
    class Config:
        from_attributes = True

class TestFeedback(BaseModel):
    feedback_general: str
    feedback_test: List[str]
    feedback_positive: str

    class Config:
        from_attributes = True
        