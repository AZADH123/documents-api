"""
====================================================================
tests/unit/test_document_service.py — unit tests for the service.
====================================================================

A "unit test" checks ONE piece of logic in isolation, with no
external dependencies. Here we test the DocumentService by giving
it a real (but tiny) InMemoryDocumentRepository.

We don't spin up FastAPI or HTTP at all — just call methods on
the service directly.
"""

import pytest

from app.domain.errors import DocumentNotFoundError
from app.repositories.in_memory import InMemoryDocumentRepository
from app.schemas.documents import DocumentCreate, DocumentUpdate
from app.services.document_service import DocumentService


# ---------- helper --------------------------------------------------
def _make_service() -> DocumentService:
    """Build a service with a fresh empty repository."""
    return DocumentService(InMemoryDocumentRepository())


# ---------- create --------------------------------------------------
def test_create_document_returns_entity_with_id():
    service = _make_service()
    doc = service.create(DocumentCreate(title="Hello", content="World"))

    assert doc.id                # an id was generated
    assert doc.title == "Hello"
    assert doc.content == "World"
    assert doc.created_at == doc.updated_at  # not updated yet


# ---------- list ----------------------------------------------------
def test_list_all_returns_every_created_document():
    service = _make_service()
    service.create(DocumentCreate(title="A"))
    service.create(DocumentCreate(title="B"))

    docs = service.list_all()
    assert len(docs) == 2
    assert {d.title for d in docs} == {"A", "B"}


# ---------- get -----------------------------------------------------
def test_get_returns_existing_document():
    service = _make_service()
    created = service.create(DocumentCreate(title="X"))

    fetched = service.get(created.id)
    assert fetched.id == created.id
    assert fetched.title == "X"


def test_get_missing_raises_not_found():
    service = _make_service()
    with pytest.raises(DocumentNotFoundError):
        service.get("does-not-exist")


# ---------- update --------------------------------------------------
def test_update_changes_only_provided_fields():
    service = _make_service()
    doc = service.create(DocumentCreate(title="Old", content="Old body"))

    updated = service.update(doc.id, DocumentUpdate(title="New"))

    assert updated.title == "New"      # changed
    assert updated.content == "Old body"  # unchanged
    assert updated.updated_at >= doc.created_at


def test_update_missing_raises_not_found():
    service = _make_service()
    with pytest.raises(DocumentNotFoundError):
        service.update("missing", DocumentUpdate(title="New"))


# ---------- delete --------------------------------------------------
def test_delete_removes_document():
    service = _make_service()
    doc = service.create(DocumentCreate(title="Bye"))

    service.delete(doc.id)

    with pytest.raises(DocumentNotFoundError):
        service.get(doc.id)


def test_delete_missing_raises_not_found():
    service = _make_service()
    with pytest.raises(DocumentNotFoundError):
        service.delete("missing")