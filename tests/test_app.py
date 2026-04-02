import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        resp = await ac.get("/activities")

        # Assert
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_prevent_duplicate():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        resp = await ac.post(f"/activities/{activity}/signup", params={"email": email})
        resp2 = await ac.post(f"/activities/{activity}/signup", params={"email": email})

        # Assert
        assert resp.status_code == 200
        assert resp2.status_code == 409
        assert "already signed up" in resp2.json()["detail"].lower()

@pytest.mark.asyncio
async def test_unregister_participant():
    # Arrange
    email = "removeuser@mergington.edu"
    activity = "Programming Class"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        resp = await ac.delete(f"/activities/{activity}/unregister", params={"email": email})
        resp2 = await ac.delete(f"/activities/{activity}/unregister", params={"email": email})

        # Assert
        assert resp.status_code == 200
        assert resp2.status_code == 404

@pytest.mark.asyncio
async def test_activity_not_found():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        resp = await ac.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
        resp2 = await ac.delete("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})

        # Assert
        assert resp.status_code == 404
        assert resp2.status_code == 404
