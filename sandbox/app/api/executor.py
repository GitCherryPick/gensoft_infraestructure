from fastapi import APIRouter
from app.core import executor
from app.schema.code_input import CodeInput, CodeInput2

router = APIRouter()

@router.post("/run", tags=["executor"])
def run_python_code(payload: CodeInput):
    result_run = executor.run_code(payload.code)
    return result_run

@router.post("/execute", tags=["executor"])
def execute_code(payload: CodeInput2):
    print("paila")
    print(payload)
    result = executor.execute_code(payload.code, payload.call)
    return result
