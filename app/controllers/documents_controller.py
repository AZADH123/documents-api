from app.domain.entities import Document
from app.schemas.documents import (
    DocumentCreateRequest,
    DocumentResponse,
    DocumentUpdateRequest,
)
from app.services.document_service import DocumentService


class DocumentsController:
    """Translates between HTTP DTOs and the service layer's domain entities.
    Holds no business rules and no route definitions."""

    def __init__(self, service: DocumentService) -> None:
        self._service = service

    @staticmethod
    def _to_response(document: Document) -> DocumentResponse:
        return DocumentResponse(
            id=document.id,
            title=document.title,
            content=document.content,
            created_at=document.created_at,
        )

    async def create(self, payload: DocumentCreateRequest) -> DocumentResponse:
        document = await self._service.create_document(payload.title, payload.content)
        return self._to_response(document)

    async def list_all(self) -> list[DocumentResponse]:
        return [self._to_response(d) for d in await self._service.list_documents()]

    async def get(self, document_id: str) -> DocumentResponse:
        return self._to_response(await self._service.get_document(document_id))

    async def replace(self, document_id: str, payload: DocumentUpdateRequest) -> DocumentResponse:
        document = await self._service.replace_document(
            document_id, payload.title, payload.content
        )
        return self._to_response(document)

    async def delete(self, document_id: str) -> None:
        await self._service.delete_document(document_id)