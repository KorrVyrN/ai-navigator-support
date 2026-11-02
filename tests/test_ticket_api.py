"""API integration tests for local ticket storage and access control."""
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("NAVIGATOR_API_TOKEN", "a" * 43)
    monkeypatch.setenv("GIGACHAT_API_KEY", "test-key")
    monkeypatch.setenv("NAVIGATOR_DATA_DIR", str(tmp_path))
    get_settings.cache_clear()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    get_settings.cache_clear()


def test_tickets_require_authentication(client):
    assert client.get("/api/v1/tickets").status_code == 401
    assert client.post("/api/v1/tickets", json={}).status_code == 401


def test_ticket_roundtrip(client):
    headers = {"Authorization": "Bearer " + "a" * 43}
    ticket = {
        "id": "ticket-1",
        "timestamp": datetime(2026, 11, 2, tzinfo=timezone.utc).isoformat(),
        "description": "Synthetic POS offline",
        "region": "Lipetsk",
        "equipment": "POS",
    }
    response = client.post("/api/v1/tickets", headers=headers, json={"ticket": ticket})
    assert response.status_code == 200
    response = client.get("/api/v1/tickets", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "ticket-1"
    ticket["description"] = "Synthetic POS restored"
    assert client.post("/api/v1/tickets", headers=headers, json={"ticket": ticket}).status_code == 200
    assert client.get("/api/v1/tickets", headers=headers).json()[0]["description"] == "Synthetic POS restored"


def test_invalid_ticket_rejected(client):
    headers = {"Authorization": "Bearer " + "a" * 43}
    response = client.post("/api/v1/tickets", headers=headers, json={"ticket": {"id": "1"}})
    assert response.status_code == 422


def test_demo_endpoint_requires_authentication(client):
    assert client.get("/api/v1/demo/tickets").status_code == 401
    response = client.get("/api/v1/demo/tickets", headers={"Authorization": "Bearer " + "a" * 43})
    assert response.status_code == 200
    assert len(response.json()) > 0
