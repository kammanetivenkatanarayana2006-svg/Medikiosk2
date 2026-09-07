import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)

def test_health_endpoint():
    """
    Test health check endpoint.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "MediKiosk Backend"

def test_api_info_endpoint():
    """
    Test API information endpoint.
    """
    response = client.get("/api/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data