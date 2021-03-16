import itertools

import pytest
from fastapi.testclient import TestClient

import api


@pytest.fixture
def client():
    return TestClient(api.main.app)


def test_should_always_pass():
    pass


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_input(client):
    data = dict(size=100_000_000, inside=70_000_000, user="aaa")
    resp = client.post("/input", json=data)
    assert resp.status_code == 200
    d = resp.json()
    assert len(d) == 1
    for v in itertools.chain(d.keys(), d.values()):
        assert isinstance(v, str)
        assert len(v) > 0
