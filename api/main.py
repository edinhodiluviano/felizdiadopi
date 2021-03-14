from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def root():
    return {}


class Result(BaseModel):
    size: int
    inside: int


@app.post("/input")
def input(result: Result):
    return {}
