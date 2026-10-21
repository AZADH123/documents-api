"""
====================================================================
tests/conftest.py — shared pytest fixtures.
====================================================================
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repositories.in_memory import (
    InMemoryDocumentRepository,
    InMemoryUserRepository,
)


@pytest.fixture
def client() -> TestClient:
    """
    A fresh TestClient wired to fresh in-memory repositories.
    Function-scoped → every test starts with empty storage.
    """
    app = create_app()
    app.state.document_repository = InMemoryDocumentRepository()
    app.state.user_repository = InMemoryUserRepository()
    return TestClient(app)


# --------------------------------------------------------------------
# Auth helper
# --------------------------------------------------------------------
@pytest.fixture
def registered_user(client: TestClient) -> dict:
    """
    Register a known user and return their credentials.
    Useful for tests that just need a user to exist.
    """
    creds = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
    }
    response = client.post("/auth/register", json=creds)
    assert response.status_code == 201, response.json()
    return creds


@pytest.fixture
def auth_token(client: TestClient, registered_user: dict) -> str:
    """
    Register a user, log in, and return a valid JWT.
    Tests that hit protected endpoints use this fixture to get a token.
    """
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200, response.json()
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Convenience: ready-to-use Authorization headers for the test client."""
    return {"Authorization": f"Bearer {auth_token}"}