"""
====================================================================
app/controllers/documents_controller.py — HTTP ↔ service translation.
====================================================================

The controller is a thin adapter:
  - Takes Pydantic DTOs in (FastAPI already validated them).
  - Calls the service.
  - Takes a domain entity out.
  - Converts it to a response DTO.

It contains NO business rules. If you find yourself writing `if`
statements about documents here, move them into the service.
"""

from fastapi import Depends

from app.dependencies import get_document_service
from app.schemas.documents import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services.document_service import DocumentService


class DocumentsController:
    """
    The controller is a class so FastAPI's Depends() can construct
    it per request and inject the service automatically.
    """

    def __init__(
        self,
        service: DocumentService = Depends(get_document_service),
    ) -> None:
        self.service = service

    # ---- create -----------------------------------------------------
    def create(self, payload: DocumentCreate) -> DocumentResponse:
        document = self.service.create(payload)
        return DocumentResponse.from_entity(document)

    # ---- read all ---------------------------------------------------
    def list_all(self) -> list[DocumentResponse]:
        return [
            DocumentResponse.from_entity(d) for d in self.service.list_all()
        ]

    # ---- read one ---------------------------------------------------
    def get(self, document_id: str) -> DocumentResponse:
        document = self.service.get(document_id)
        return DocumentResponse.from_entity(document)

    # ---- update -----------------------------------------------------
    def update(
        self, document_id: str, payload: DocumentUpdate
    ) -> DocumentResponse:
        document = self.service.update(document_id, payload)
        return DocumentResponse.from_entity(document)

    # ---- delete -----------------------------------------------------
    def delete(self, document_id: str) -> None:
        self.service.delete(document_id)