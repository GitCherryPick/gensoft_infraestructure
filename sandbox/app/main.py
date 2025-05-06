from fastapi import FastAPI
from pydantic import BaseModel
from .api import submissions 
from .core import executor
from app.database import engine
from app.models.base import Base

app = FastAPI()

app.include_router(submissions.router)
Base.metadata.create_all(bind=engine)

class CodeInput(BaseModel):
    code: str

class CodeInput2(CodeInput):
    call: str

@app.get("/")
def root():
    return {"message": "Hi World from Sandbox!"}

@app.post("/run")
def run_python_code(payload: CodeInput):
    stdout, stderr = executor.run_code(payload.code)
    return {"output": stdout, "errors": stderr}

@app.post("/execute")
def execute_code(payload: CodeInput2):
    result = executor.execute_code(payload.code, payload.call)
    return result

