import os
import datetime as dt
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


@app.get("/")
def root():
    return {}


class Result(BaseModel):
    size: int
    inside: int

    class Config:
        extra = "forbid"


@app.post("/input")
def input(result: Result):
    return {}


class Config:
    data = Path("./data")


class ResultSave(Result):
    timestamp: str = Field(default_factory=dt.datetime.utcnow)

    def line(self):
        return self.json() + "\n"


def save(result: Result):
    result_save = ResultSave(**result.dict())
    line = result_save.line()
    file = filename()
    with open(file, "a") as f:
        f.write(line)
    return file


def filename():
    pid = os.getpid()
    return Config().data / f"{pid}.jsonl"
