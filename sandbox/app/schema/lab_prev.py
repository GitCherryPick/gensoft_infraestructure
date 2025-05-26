from typing import List, Optional
from pydantic import BaseModel

class LabRequest(BaseModel):
    codigo_estudiante: str
    enunciado: str
    llamada_funcion: str
    resultado_obtenido: str

class ErrorFeedback(BaseModel):
    error: str
    line: int

    class Config:
        from_attributes = True

class LabFeedback(BaseModel):
    feedback_docente: str
    warnings: Optional[List[str]]
    errores: Optional[ErrorFeedback]
    
    class Config:
        from_attributes = True