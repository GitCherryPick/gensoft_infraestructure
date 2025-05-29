from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union, Any
from datetime import datetime
import json

class ReplicationSubmissionBase(BaseModel):
    user_id: int
    exercise_id: int
    student_code: str
    typing_duration_seconds: int
    errores_sintacticos: Union[List[str], str]
    ejecucion_simulada_exitosa: bool
    estructura_igual_a_objetivo: bool
    puntaje_similitud: float
    diferencias_detectadas: Union[List[str], str]
    pistas_generadas: Union[List[str], str]
    is_passed: bool
    
    @validator('errores_sintacticos', pre=True)
    def parse_errores_sintacticos(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
        
    @validator('diferencias_detectadas', pre=True)
    def parse_diferencias_detectadas(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
        
    @validator('pistas_generadas', pre=True)
    def parse_pistas_generadas(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

class ReplicationSubmissionCreate(ReplicationSubmissionBase):
    pass

class ReplicationSubmissionUpdate(BaseModel):
    student_code: Optional[str] = None
    typing_duration_seconds: Optional[int] = None
    errores_sintacticos: Optional[Union[List[str], str]] = None
    ejecucion_simulada_exitosa: Optional[bool] = None
    estructura_igual_a_objetivo: Optional[bool] = None
    puntaje_similitud: Optional[float] = None
    diferencias_detectadas: Optional[Union[List[str], str]] = None
    pistas_generadas: Optional[Union[List[str], str]] = None
    is_passed: Optional[bool] = None

    # Validadores para los campos que pueden venir como JSON
    @validator('errores_sintacticos', pre=True)
    def parse_errores_sintacticos(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
        
    @validator('diferencias_detectadas', pre=True)
    def parse_diferencias_detectadas(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
        
    @validator('pistas_generadas', pre=True)
    def parse_pistas_generadas(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

class ReplicationSubmissionOut(ReplicationSubmissionBase):
    id: int
    submission_date: datetime

    class Config:
        from_attributes = True
