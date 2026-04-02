
import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_get_activities():
    # Arrange
    client = TestClient(app)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_prevent_duplicate():
    # Arrange
    client = TestClient(app)
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert resp2.status_code == 409
    assert "already signed up" in resp2.json()["detail"].lower()

def test_unregister_participant():
    # Arrange
    client = TestClient(app)
    email = "removeuser@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    resp = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    resp2 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert resp2.status_code == 404

def test_activity_not_found():
    # Arrange
    client = TestClient(app)
    # Act
    resp = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    resp2 = client.delete("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})
    # Assert
    assert resp.status_code == 404
    assert resp2.status_code == 404
