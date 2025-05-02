from fastapi import FastAPI
from pydantic import BaseModel
from .core import executor
app = FastAPI()

class CodeInput(BaseModel):
    code: str

@app.get("/")
def root():
    return {"message": "Hi World from Sandbox!"}

@app.post("/run")
def run_python_code(payload: CodeInput):
    stdout, stderr = executor.run_code(payload.code)
    return {"output": stdout, "errors": stderr}