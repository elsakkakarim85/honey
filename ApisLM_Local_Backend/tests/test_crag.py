import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_chat_endpoint_fallback():
    """Verify that the AI falls back gracefully if LlamaCpp is offline."""
    response = client.post("/api/chat", json={"query": "How do I treat varroa?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Offline AI backend is running in fallback mode" in data["response"] or data["response"] != ""

def test_climate_endpoint():
    """Verify microclimate fetching endpoint structure."""
    response = client.post("/api/climate", json={"latitude": 45.0, "longitude": 9.0})
    assert response.status_code == 200
    data = response.json()
    assert "climate_data" in data
    assert "foraging_score" in data["climate_data"]
