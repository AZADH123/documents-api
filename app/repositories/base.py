"""
====================================================================
app/repositories/base.py — the repository contract.
====================================================================

A `Protocol` in Python is like an interface in TypeScript or Java:
it describes WHAT methods a class must have, without saying HOW
they work.

Any class that has these methods is automatically considered a
DocumentRepository — we don't need to inherit from it explicitly.
This is called "structural typing" or "duck typing with a contract".

Today we implement it with an in-memory dict. Tomorrow we'll
write a PostgresDocumentRepository with the SAME methods. The
service layer doesn't care which one is plugged in.
"""

from typing import Protocol

from app.domain.entities import Document


class DocumentRepository(Protocol):
    """The persistence contract for documents."""

    def add(self, document: Document) -> None:
        """Insert a new document. Raises if id already exists."""
        ...

    def get(self, document_id: str) -> Document | None:
        """Return the document with this id, or None if missing."""
        ...

    def list_all(self) -> list[Document]:
        """Return all documents."""
        ...

    def delete(self, document_id: str) -> bool:
        """Delete by id. Return True if something was deleted, False otherwise."""
        ...

    def exists(self, document_id: str) -> bool:
        """True if a document with this id exists."""