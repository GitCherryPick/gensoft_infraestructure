from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime 

class HintBase(BaseModel):
    task_id: Optional[int] = Field(None, description="ID of the task this hint belongs to.")
    hint_order: int = Field(..., description="The sequential order of the hint within its task.")
    hint_text: str = Field(..., description="The textual content of the hint.")
    penalty_points: int = Field(0, description="Points deducted for using this hint.")

class HintCreate(HintBase):
    pass

class HintUpdate(BaseModel):
    task_id: Optional[int] = Field(None, description="Updates the ID of the associated task.")
    hint_order: Optional[int] = Field(None, description="Updates the sequential order of the hint.")
    hint_text: Optional[str] = Field(None, description="Updates the content of the hint.")
    penalty_points: Optional[int] = Field(None, description="Updates the penalty points for this hint.")

class HintOut(HintBase):
    hint_id: int = Field(..., description="The unique, auto-generated ID of the hint.")
    class Config:
        from_attributes = True