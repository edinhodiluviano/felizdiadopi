from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api import main


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def mock_db():
    with patch("api.main.db") as m:
        yield m


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_root_doesnt_call_db(client, mock_db):
    _ = client.get("/")
    assert len(mock_db.method_calls) == 0


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
    data = dict(size=100_000_000, inside=70_000_000, user="aaa")
    resp = client.post("/input", json=data)
    assert resp.status_code == 200


def test_input_calls_db(client, mock_db):
    data = dict(size=100_000_000, inside=70_000_000, user="aaa")
    _ = client.post("/input", json=data)
    assert len(mock_db.method_calls) > 0


def test_random_phrase(client):
    data = dict(size=100_000_000, inside=70_000_000, user="aaa")
    resp = client.post("/input", json=data)
    assert len(resp.json()) == 1
