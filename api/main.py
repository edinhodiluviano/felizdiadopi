from fastapi import FastAPI

from .model import Result
from .db import save


app = FastAPI()


@app.get("/")
def root():
    return {}


@app.post("/input")
def input(result: Result):
    save(result)
    return {}
