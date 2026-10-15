API = "/api/v1/documents"


def create_doc(client, title="A", content="body"):
    response = client.post(API, json={"title": title, "content": content})
    assert response.status_code == 201
    return response.json()


def test_create_returns_201_with_generated_fields(client):
    body = create_doc(client, "First doc", "Hello")
    assert set(body) == {"id", "title", "content", "createdAt"}
    assert body["title"] == "First doc"


def test_list_preserves_creation_order(client):
    create_doc(client, "A")
    create_doc(client, "B")
    assert [d["title"] for d in client.get(API).json()] == ["A", "B"]


def test_get_round_trips(client):
    created = create_doc(client)
    response = client.get(f"{API}/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_returns_404_error_envelope(client):
    response = client.get(f"{API}/does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "DOCUMENT_NOT_FOUND"
    assert "does-not-exist" in body["error"]["message"]


def test_put_replaces_and_keeps_created_at(client):
    created = create_doc(client, "Old", "old body")
    response = client.put(f"{API}/{created['id']}", json={"title": "New", "content": "new body"})
    assert response.status_code == 200
    assert response.json()["createdAt"] == created["createdAt"]
    assert response.json()["title"] == "New"


def test_delete_returns_204_then_404(client):
    created = create_doc(client)
    assert client.delete(f"{API}/{created['id']}").status_code == 204
    assert client.get(f"{API}/{created['id']}").status_code == 404


def test_health_endpoints(client):
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 200


def test_unknown_field_rejected_with_error_envelope(client):
    response = client.post(API, json={"title": "A", "content": "c", "author": "hacker"})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert any(d["field"].endswith("author") for d in error["details"])


def test_title_length_rules_enforced(client):
    assert client.post(API, json={"title": "", "content": "c"}).status_code == 422
    assert client.post(API, json={"title": "x" * 201, "content": "c"}).status_code == 422
    assert client.post(API, json={"content": "c"}).status_code == 422