import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client():
    return TestClient(app)


def test_basic(client):
    response = client.get("/")
    assert response.status_code == 200


def test_input_returns_error_when_get(client):
    resp = client.get("/input")
    assert resp.status_code == 405


def test_input_returns_422_when_post_with_no_input(client):
    resp = client.post("/input")
    assert resp.status_code == 422


def test_input_returns_200_when_post_with_good_input(client):
    data = dict(size=100_000_000, inside=70_000_000)
    resp = client.post("/input", json=data)
    assert resp.status_code == 200
