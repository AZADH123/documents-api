import asyncio

import pytest

from app.domain.errors import DocumentNotFoundError
from app.repositories.in_memory import InMemoryDocumentRepository
from app.services.document_service import DocumentService

API = "/api/v1/documents"


def make_service() -> DocumentService:
    return DocumentService(InMemoryDocumentRepository())


def test_create_generates_id_and_utc_timestamp():
    document = asyncio.run(make_service().create_document("Title", "Body"))
    assert document.id
    assert document.created_at.tzinfo is not None
    assert (document.title, document.content) == ("Title", "Body")


def test_get_missing_raises_domain_error():
    with pytest.raises(DocumentNotFoundError):
        asyncio.run(make_service().get_document("nope"))


def test_replace_preserves_created_at():
    service = make_service()
    created = asyncio.run(service.create_document("Old", "old body"))
    replaced = asyncio.run(service.replace_document(created.id, "New", "new body"))
    assert replaced.created_at == created.created_at
    assert replaced.title == "New"


def test_delete_then_get_raises():
    service = make_service()
    created = asyncio.run(service.create_document("A", "body"))
    asyncio.run(service.delete_document(created.id))
    with pytest.raises(DocumentNotFoundError):
        asyncio.run(service.get_document(created.id))