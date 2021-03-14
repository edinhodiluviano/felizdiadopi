from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def root():
    return {}


class Result(BaseModel):
    size: int
    inside: int


@app.post("/data")
def data(result: Result):
    return {}
