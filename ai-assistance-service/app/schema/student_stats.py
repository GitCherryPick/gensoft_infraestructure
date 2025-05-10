from pydantic import BaseModel, field_validator
from typing import Any, List, Dict, Optional
from datetime import datetime

class StudentStatsBase(BaseModel):
    student_id: int
    total_activities_answered: Optional[int] = 0
    common_mistakes: Optional[Dict[str, Any]] = {}
    interests: Optional[List[str]] = []
    performance_stats: Optional[Dict[str, Any]] = None

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

    @field_validator("performance_stats", pre=True, always=True)
    def validate_performance_stats(cls, value):
        if value is not None and not isinstance(value, dict):
            raise ValueError("performance_stats must be a dictionary")
        return value


class StudentStatsRequest(StudentStatsBase):
    pass


class StudentStatsUpdateRequest(BaseModel):
    total_activities_answered: Optional[int]
    common_mistakes: Optional[Dict[str, Any]]
    interests: Optional[List[str]]
    performance_stats: Optional[Dict[str, Any]]


class StudentStatsResponse(StudentStatsBase):
    id: int
    last_accessed: datetime

    class Config:
        from_attributes = True