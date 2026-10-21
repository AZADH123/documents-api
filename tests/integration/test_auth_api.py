"""
====================================================================
tests/integration/test_auth_api.py — HTTP-level tests for auth.
====================================================================
"""

from fastapi.testclient import TestClient


# ---------- /auth/register -----------------------------------------
def test_register_returns_201_and_user_without_password(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_rejects_short_password(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "123",  # min is 6
        },
    )
    assert response.status_code == 422


def test_register_rejects_invalid_email(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "alice",
            "email": "not-an-email",
            "password": "password123",
        },
    )
    assert response.status_code == 422


def test_register_rejects_duplicate_email(client: TestClient):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=payload)
    # Same email, different username
    payload["username"] = "alice2"
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["error"] == "UserAlreadyExistsError"


# ---------- /auth/login --------------------------------------------
def test_login_returns_token(client: TestClient, registered_user: dict):
    response = client.post(
        "/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["expires_in"] > 0


def test_login_wrong_password_returns_401(client: TestClient, registered_user: dict):
    response = client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": "WRONG"},
    )
    assert response.status_code == 401
    assert response.json()["error"] == "InvalidCredentialsError"


def test_login_unknown_email_returns_401(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": "ghost@example.com", "password": "whatever"},
    )
    assert response.status_code == 401


# ---------- /auth/me (PROTECTED) -----------------------------------
def test_me_with_valid_token_returns_user(client: TestClient, auth_headers: dict):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"


def test_me_without_token_returns_401(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["error"] == "InvalidTokenError"


def test_me_with_garbage_token_returns_401(client: TestClient):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert response.status_code == 401


def test_me_without_bearer_prefix_returns_401(client: TestClient, auth_token: str):
    response = client.get(
        "/auth/me",
        headers={"Authorization": auth_token},  # missing "Bearer "
    )
    assert response.status_code == 401


# ---------- /documents now requires auth ---------------------------
def test_documents_rejects_request_without_token(client: TestClient):
    response = client.get("/documents/")
    assert response.status_code == 401