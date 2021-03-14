import json
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
    with patch("api.config.Config", return_value=config_instance):
        yield config_instance


def test_config(config):
    assert len(str(config.data)) > 15
    assert len(list(config.data.glob("*"))) == 0


def test_save_results(config):
    result = api.model.Result(size=10_000_000, inside=6_000_000, user="aaa")
    file = api.db.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    assert files[0] == file


def test_save_only_one_file(config):
    for size in range(1_000_000, 11_000_000, 1_000_000):
        result = api.main.Result(size=size, inside=6_000_000, user="aaa")
        api.db.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    # basically a new test here... just saving some io time
    with open(files[0]) as f:
        lines = f.read()
    lines = lines.splitlines()
    assert len(lines) == 10


def test_save_format(config):
    result = api.model.Result(size=10_000_000, inside=6_000_000, user="aaa")
    file = api.db.save(result)
    with open(file) as f:
        lines = f.read()
    lines = lines.splitlines()
    d = json.loads(lines[0])
    assert len(d) == 4
    assert "user" in d
    assert "size" in d
    assert "inside" in d
    assert "timestamp" in d
    d = dt.datetime.fromisoformat(d["timestamp"])
    assert 1990 < d.year < 2050
    delta = dt.datetime.utcnow() - d
    assert 0 < delta.total_seconds() < 1
