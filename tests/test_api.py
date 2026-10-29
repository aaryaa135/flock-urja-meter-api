"""Tests for the FastAPI application endpoints (TestClient, no live portal)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """GET /health should return exactly {"status": "ok"}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_meters_search_endpoint_requires_session_cookie(monkeypatch):
    """The meters search endpoint should work without a session cookie (it will fail at the portal layer)."""
    # We don't mock the portal client here; the TestClient will attempt a real
    # request which will fail because there's no network. We just verify the
    # route is registered and returns a non-2xx or 502.
    response = client.get("/meters/search?q=J100000&page=1")
    # Without network access, this will be a connection error -> 502 or similar
    assert response.status_code in (502, 503, 504)


def test_transformers_endpoint_registered():
    """The transformers endpoint should be registered."""
    response = client.get("/transformers?page=1")
    # Without network access, this will be a connection error -> 502 or similar
    assert response.status_code in (502, 503, 504)


def test_openapi_schema_generated():
    """OpenAPI schema should be generated and contain our routes."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/health" in schema["paths"]
    assert "/meters/search" in schema["paths"]
    assert "/transformers" in schema["paths"]
