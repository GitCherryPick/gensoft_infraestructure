from pydantic import BaseModel

class ResultReplicator(BaseModel):
    codigo_estudiante: str
    codigo_objetivo: str
    consignas_docente: str
    contexto_ejercicio: str

    class Config:
        from_attributes = True