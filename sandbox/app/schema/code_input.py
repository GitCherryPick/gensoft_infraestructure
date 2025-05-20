from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str

class CodeInput2(CodeInput):
    call: str