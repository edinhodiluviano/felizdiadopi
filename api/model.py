import datetime as dt

from pydantic import BaseModel, Field


class Result(BaseModel):
    size: int
    inside: int
    user: str

    class Config:
        extra = "forbid"


class ResultSave(Result):
    timestamp: str = Field(default_factory=dt.datetime.utcnow)
