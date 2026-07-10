from pydantic import BaseModel, Field
from typing import Any, Optional


class CreateTeam(BaseModel):
    country_name : str = Field(min_length=1)
    coach_name : str = Field(min_length=1)
    group_name : str = Field(min_length=1)
    points : int = Field(gt=0)


class UpdateTeam(BaseModel):
    country_name : str = Field(min_length=1)
    coach_name : str = Field(min_length=1)
    group_name : str = Field(min_length=1)
    points : int = Field(gt=0)


class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str
    path: str


