from pydantic import BaseModel
from typing import Optional
class Submission(BaseModel):
    UserId: Optional[int] = None
    code: str
    taskId: int