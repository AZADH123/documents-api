"""
====================================================================
app/services/document_service.py — business rules.
====================================================================

The service layer is where the actual business logic lives.
It is the ONLY layer that knows the rules:
  - "When creating a document, generate an id and timestamps."
  - "When updating, only the supplied fields change."
  - "When fetching a missing id, raise DocumentNotFoundError."

The service depends on the repository (via the Protocol in base.py),
so it doesn't know or care whether documents are stored in memory,
Postgres, or a file. This is called "dependency inversion":
the high-level policy (service) doesn't depend on the low-level
detail (storage); both depend on an abstraction (the Protocol).

The service has NO knowledge of HTTP. It can be reused from a CLI,
a background job, a test — anything.
"""

from app.domain.entities import Document
from app.domain.errors import DocumentNotFoundError
from app.repositories.base import DocumentRepository
from app.schemas.documents import DocumentCreate, DocumentUpdate


class DocumentService:
    """Apply business rules to documents."""

    def __init__(self, repository: DocumentRepository) -> None:
        # We store the injected repository; never reach for a global.
        self.repository = repository

    # ---- create -----------------------------------------------------
    def create(self, payload: DocumentCreate) -> Document:
        document = Document.new(
            title=payload.title,
            content=payload.content,
        )
        self.repository.add(document)
        return document

    # ---- read -------------------------------------------------------
    def list_all(self) -> list[Document]:
        return self.repository.list_all()

    def get(self, document_id: str) -> Document:
        document = self.repository.get(document_id)
        if document is None:
            raise DocumentNotFoundError(
                f"Document with id '{document_id}' not found"
            )
        return document

    # ---- update -----------------------------------------------------
    def update(self, document_id: str, payload: DocumentUpdate) -> Document:
        # Reuse get() so we get the not-found error for free.
        document = self.get(document_id)
        document.update(title=payload.title, content=payload.content)
        # NOTE: the in-memory repo already holds a reference to this
        # object, so no explicit save is needed. A real DB repo would
        # persist here.
        return document

    # ---- delete -----------------------------------------------------
    def delete(self, document_id: str) -> None:
        if not self.repository.delete(document_id):
            raise DocumentNotFoundError(
                f"Document with id '{document_id}' not found"
            )