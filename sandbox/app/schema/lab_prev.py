from typing import List, Optional
from pydantic import BaseModel

class LabBase(BaseModel):
    codigo_estudiante: str
    enunciado: str

class LabRequest(LabBase):
    llamada_funcion: str
    resultado_obtenido: str

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

class Test(BaseModel):
    input: str
    expected_output: str
    real_output: Optional[str] = ""

class LabTestRequest(LabBase):
    test_set: List[Test]
    
class TestFeedback(BaseModel):
    feedback_general: str
    feedback_test: List[str]
    feedback_positive: str
    errores: Optional[ErrorFeedback]

    class Config:
        from_attributes = True