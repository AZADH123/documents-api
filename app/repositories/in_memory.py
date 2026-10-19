"""
====================================================================
app/repositories/in_memory.py — dict-backed repository.
====================================================================

This is the simplest possible implementation of DocumentRepository:
it stores documents in a Python dict that lives in process memory.

Why bother? Because it lets us build and test the ENTIRE app
end-to-end without standing up a database. Once the rest of the
app works, we can swap this for a real DB-backed repository and
nothing else has to change.

⚠️ Memory is wiped on every restart. Don't use this in production.
"""

from app.domain.entities import Document
from app.domain.errors import DuplicateDocumentError


class InMemoryDocumentRepository:
    """Dict-backed implementation of DocumentRepository."""

    def __init__(self) -> None:
        # Keys are document ids, values are Document entities.
        self._store: dict[str, Document] = {}

    def add(self, document: Document) -> None:
        if document.id in self._store:
            raise DuplicateDocumentError(
                f"Document with id '{document.id}' already exists"
            )
        self._store[document.id] = document

    def get(self, document_id: str) -> Document | None:
        return self._store.get(document_id)

    def list_all(self) -> list[Document]:
        # Return a copy so callers can't mutate our internal store.
        return list(self._store.values())

    def delete(self, document_id: str) -> bool:
        if document_id in self._store:
            del self._store[document_id]
            return True
        return False

    def exists(self, document_id: str) -> bool:
        return document_id in self._store