"""
====================================================================
tests/integration/test_documents_api.py — HTTP-level tests for /documents.
====================================================================

NOTE: All /documents endpoints are now PROTECTED.
Every test uses the `auth_headers` fixture (see conftest.py),
which registers a user, logs in, and returns a ready-to-use
Authorization header.
"""

from fastapi.testclient import TestClient


# ---------- CREATE --------------------------------------------------
def test_create_document_returns_201(client: TestClient, auth_headers: dict):
    response = client.post(
        "/documents/",
        headers=auth_headers,
        json={"title": "Doc 1", "content": "Hello"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["title"] == "Doc 1"
    assert body["content"] == "Hello"
    assert "created_at" in body


def test_create_document_rejects_empty_title(client: TestClient, auth_headers: dict):
    response = client.post(
        "/documents/",
        headers=auth_headers,
        json={"title": "", "content": ""},
    )
    assert response.status_code == 422


# ---------- LIST ----------------------------------------------------
def test_list_documents_returns_all(client: TestClient, auth_headers: dict):
    client.post("/documents/", headers=auth_headers, json={"title": "A"})
    client.post("/documents/", headers=auth_headers, json={"title": "B"})

    response = client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_documents_starts_empty(client: TestClient, auth_headers: dict):
    response = client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


# ---------- GET ONE -------------------------------------------------
def test_get_document_by_id(client: TestClient, auth_headers: dict):
    create = client.post(
        "/documents/", headers=auth_headers, json={"title": "Find me"}
    )
    doc_id = create.json()["id"]

    response = client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_missing_returns_404_envelope(client: TestClient, auth_headers: dict):
    response = client.get("/documents/missing-id", headers=auth_headers)
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "DocumentNotFoundError"
    assert "message" in body


# ---------- UPDATE --------------------------------------------------
def test_update_document(client: TestClient, auth_headers: dict):
    create = client.post(
        "/documents/",
        headers=auth_headers,
        json={"title": "Old", "content": "old"},
    )
    doc_id = create.json()["id"]

    response = client.put(
        f"/documents/{doc_id}",
        headers=auth_headers,
        json={"title": "New"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["content"] == "old"


def test_update_missing_returns_404(client: TestClient, auth_headers: dict):
    response = client.put(
        "/documents/missing",
        headers=auth_headers,
        json={"title": "X"},
    )
    assert response.status_code == 404


# ---------- DELETE --------------------------------------------------
def test_delete_document(client: TestClient, auth_headers: dict):
    create = client.post("/documents/", headers=auth_headers, json={"title": "Temp"})
    doc_id = create.json()["id"]

    response = client.delete(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/documents/{doc_id}", headers=auth_headers)
    assert response.status_code == 404


def test_delete_missing_returns_404(client: TestClient, auth_headers: dict):
    response = client.delete("/documents/missing", headers=auth_headers)
    assert response.status_code == 404


# ---------- HEALTH (still public) ----------------------------------
def test_healthz(client: TestClient):
    assert client.get("/healthz").status_code == 200


def test_readyz(client: TestClient):
    assert client.get("/readyz").status_code == 200