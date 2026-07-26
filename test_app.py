import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app


def test_home_status_code():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_home_returns_json():
    client = app.test_client()
    response = client.get("/")
    data = response.get_json()
    assert data["status"] == "running"


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
