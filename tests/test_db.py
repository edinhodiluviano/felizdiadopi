import csv
import datetime as dt
from pathlib import Path
from unittest.mock import patch

import pytest

import api


@pytest.fixture(autouse=True, scope="function")
def config(tmpdir):
    class TestConfig:
        data = Path(tmpdir)

    config_instance = TestConfig()
    with patch("api.db.config") as m:
        m.Config.return_value = config_instance
        yield config_instance


def test_config(config):
    assert len(str(config.data)) > 15
    assert len(list(config.data.glob("*"))) == 0


def test_filename(config):
    print(f"{api.db.filename()=}")
    print(f"{config.data=}")
    assert str(api.db.filename()).startswith(str(config.data))


def test_save_results(config):
    result = api.model.Result(size=10_000_000, inside=6_000_000, user="bbb")
    file = api.db.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    assert files[0] == file


def test_save_only_one_file(config):
    for size in range(1_000_000, 11_000_000, 1_000_000):
        result = api.main.Result(size=size, inside=6_000_000, user="ccc")
        api.db.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    # basically a new test here... just saving some io time
    with open(files[0]) as f:
        reader = csv.DictReader(f)
        lines = [line for line in reader]
    print(f"{lines=}")
    assert len(lines) == 10


def test_save_format(config):
    result = api.model.Result(size=10_000_000, inside=6_000_000, user="ddd")
    file = api.db.save(result)
    with open(file) as f:
        reader = csv.DictReader(f)
        lines = [line for line in reader]
    print(file)
    print(lines)
    line = lines[0]
    assert len(line) == 4
    assert "user" in line
    assert "size" in line
    assert "inside" in line
    assert "timestamp" in line
    d = dt.datetime.fromisoformat(line["timestamp"])
    assert 1990 < d.year < 2050
    delta = dt.datetime.utcnow() - d
    assert 0 < delta.total_seconds() < 1
