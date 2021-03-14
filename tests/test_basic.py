import json
import datetime as dt
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api import main


@pytest.fixture
def client():
    return TestClient(main.app)


def test_basic(client):
    response = client.get("/")
    assert response.status_code == 200


def test_input_returns_error_when_get(client):
    resp = client.get("/input")
    assert resp.status_code == 405


def test_input_returns_422_when_post_with_no_input(client):
    resp = client.post("/input")
    assert resp.status_code == 422


def test_input_returns_422_if_timestamp_is_sent(client):
    data = dict(
        size=100_000_000,
        inside=70_000_000,
        timestamp="2021-03-14T02:29:19.194007",
    )
    resp = client.post("/input", json=data)
    assert resp.status_code == 422


def test_input_returns_200_when_post_with_good_input(client):
    data = dict(size=100_000_000, inside=70_000_000)
    resp = client.post("/input", json=data)
    assert resp.status_code == 200


@pytest.fixture(autouse=True, scope="function")
def config(tmpdir):
    class TestConfig:
        data = Path(tmpdir)

    config_instance = TestConfig()
    with patch("api.main.Config", return_value=config_instance):
        yield config_instance


def test_config(config):
    assert len(str(config.data)) > 15
    assert len(list(config.data.glob("*"))) == 0


def test_save_results(config):
    result = main.Result(size=10_000_000, inside=6_000_000)
    file = main.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    assert files[0] == file


def test_save_only_one_file(config):
    for size in range(1_000_000, 11_000_000, 1_000_000):
        result = main.Result(size=size, inside=6_000_000)
        main.save(result)
    files = list(config.data.glob("*"))
    assert len(files) == 1
    # basically a new test here... just saving some io time
    with open(files[0]) as f:
        lines = f.read()
    lines = lines.splitlines()
    assert len(lines) == 10


def test_save_format(config):
    result = main.Result(size=10_000_000, inside=6_000_000)
    file = main.save(result)
    with open(file) as f:
        lines = f.read()
    lines = lines.splitlines()
    d = json.loads(lines[0])
    assert "size" in d
    assert "inside" in d
    assert "timestamp" in d
    d = dt.datetime.fromisoformat(d["timestamp"])
    assert 1990 < d.year < 2050
    delta = dt.datetime.utcnow() - d
    assert 0 < delta.total_seconds() < 1
