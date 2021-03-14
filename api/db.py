import os

from . import model, config


def save(result: model.Result):
    result_save = model.ResultSave(**result.dict())
    line = result_save.line()
    file = filename()
    with open(file, "a") as f:
        f.write(line)
    return file


def filename():
    pid = os.getpid()
    return config.Config().data / f"{pid}.jsonl"
