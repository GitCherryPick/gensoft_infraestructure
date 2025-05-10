from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional
from datetime import datetime

@field_validator("common_mistakes", pre=True, always=True)
def validate_common_mistakes(cls, value):
    if value is not None and not isinstance(value, dict):
        raise ValueError("common_mistakes must be a dictionary")
    return value

@field_validator("interests", pre=True, always=True)
def validate_interests(cls, value):
    if value is not None and not all(isinstance(i, str) for i in value):
        raise ValueError("All interests must be strings")
    return value

@field_validator(pre=True)
def validate_performance_stats(cls, values):
    performance_stats = values.get("performance_stats")
    if performance_stats is not None and not isinstance(performance_stats, dict):
        raise ValueError("performance_stats must be a dictionary")
    return values

class StudentStats(BaseModel):
    student_id: int

class StudentStatsRequest(StudentStats):
    common_mistakes: Optional[Dict] = None
    interests: Optional[List[str]] = None
    performance_stats: Optional[Dict] = None
    last_accessed: datetime

    class Config:
        from_attributes = True

class StudentStatsResponse(StudentStats):
    id: int
    total_activities_answered: int
    common_mistakes: Optional[Dict] = None
    interests: Optional[List[str]] = None
    performance_stats: Optional[Dict] = None
    last_accessed: datetime

    class Config:
        from_attributes = True