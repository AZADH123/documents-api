"""
====================================================================
tests/integration/test_documents_api.py — HTTP-level tests.
====================================================================

An "integration test" exercises multiple layers wired together.
Here we hit the FastAPI app through its HTTP surface using
TestClient (which wraps httpx). No network is involved — calls
go straight to the app in-process.

These tests verify the full request/response cycle:
  - URL routing
  - Pydantic validation
  - Controller → Service → Repository
  - Exception → HTTP error mapping
"""

from fastapi.testclient import TestClient


# ---------- CREATE --------------------------------------------------
def test_create_document_returns_201(client: TestClient):
    response = client.post(
        "/documents/", json={"title": "Doc 1", "content": "Hello"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["title"] == "Doc 1"
    assert body["content"] == "Hello"
    assert "created_at" in body


def test_create_document_rejects_empty_title(client: TestClient):
    response = client.post("/documents/", json={"title": "", "content": ""})
    assert response.status_code == 422  # Pydantic validation error


# ---------- LIST ----------------------------------------------------
def test_list_documents_returns_all(client: TestClient):
    client.post("/documents/", json={"title": "A"})
    client.post("/documents/", json={"title": "B"})

    response = client.get("/documents/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_documents_starts_empty(client: TestClient):
    response = client.get("/documents/")
    assert response.status_code == 200
    assert response.json() == []


# ---------- GET ONE -------------------------------------------------
def test_get_document_by_id(client: TestClient):
    create = client.post("/documents/", json={"title": "Find me"})
    doc_id = create.json()["id"]

    response = client.get(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_missing_returns_404_envelope(client: TestClient):
    response = client.get("/documents/missing-id")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "DocumentNotFoundError"
    assert "message" in body


# ---------- UPDATE --------------------------------------------------
def test_update_document(client: TestClient):
    create = client.post("/documents/", json={"title": "Old", "content": "old"})
    doc_id = create.json()["id"]

    response = client.put(
        f"/documents/{doc_id}", json={"title": "New"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New"
    assert body["content"] == "old"  # unchanged


def test_update_missing_returns_404(client: TestClient):
    response = client.put("/documents/missing", json={"title": "X"})
    assert response.status_code == 404


# ---------- DELETE --------------------------------------------------
def test_delete_document(client: TestClient):
    create = client.post("/documents/", json={"title": "Temp"})
    doc_id = create.json()["id"]

    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 204

    # Subsequent GET should now 404
    response = client.get(f"/documents/{doc_id}")
    assert response.status_code == 404


def test_delete_missing_returns_404(client: TestClient):
    response = client.delete("/documents/missing")
    assert response.status_code == 404


# ---------- HEALTH --------------------------------------------------
def test_healthz(client: TestClient):
    assert client.get("/healthz").status_code == 200


def test_readyz(client: TestClient):
    assert client.get("/readyz").status_code == 200