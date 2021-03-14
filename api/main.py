from fastapi import FastAPI

from .model import Result


app = FastAPI()


@app.get("/")
def root():
    return {}


@app.post("/input")
def input(result: Result):
    return {}
