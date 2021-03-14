import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client():
    return TestClient(app)


def test_basic(client):
    response = client.get("/")
    assert response.status_code == 200
