from fastapi import APIRouter
from app.core import executor
from app.schema.submission import Submission
from app.api.executor import execute_code

from app.schema.code_input import CodeInput, CodeInput2
router = APIRouter()

@router.get("/prueba")
def prueba():
    return "pruebia"

@router.post("/enviar")
def enviar(submission: Submission):
    code_input_2_object = CodeInput2(code=submission.code, call="suma(1,2)")
    result = execute_code(code_input_2_object)
    return result