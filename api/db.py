import os
import csv

from . import model, config


def save(result: model.Result):
    result_save = model.ResultSave(**result.dict())
    file = filename()

    new = not file.exists()

    with open(file, "a") as f:
        fieldnames = result_save.dict().keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if new:
            writer.writeheader()
        writer.writerow(result_save.dict())
    return file


def filename():
    pid = os.getpid()
    return config.Config().data / f"{pid}.jsonl"
