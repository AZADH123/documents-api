import logging
import uuid
from datetime import datetime, timezone

from app.domain.entities import Document
from app.domain.errors import DocumentNotFoundError
from app.repositories.base import DocumentRepository

logger = logging.getLogger(__name__)


class DocumentService:
    """Business rules. Knows nothing about HTTP or Pydantic."""

    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    async def create_document(self, title: str, content: str) -> Document:
        # When the DB lands it may generate ids itself — that change is
        # isolated to this method plus the new repository.
        document = Document(
            id=uuid.uuid4().hex,
            title=title,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        created = await self._repository.add(document)
        logger.info("document created id=%s", created.id)
        return created

    async def get_document(self, document_id: str) -> Document:
        document = await self._repository.get(document_id)
        if document is None:
            raise DocumentNotFoundError(document_id)
        return document

    async def list_documents(self) -> list[Document]:
        return await self._repository.list_all()

    async def replace_document(self, document_id: str, title: str, content: str) -> Document:
        existing = await self.get_document(document_id)   # raises 404 if missing
        updated = Document(
            id=existing.id,
            title=title,
            content=content,
            created_at=existing.created_at,   # createdAt is immutable
        )
        await self._repository.save(updated)
        return updated

    async def delete_document(self, document_id: str) -> None:
        deleted = await self._repository.delete(document_id)
        if not deleted:
            raise DocumentNotFoundError(document_id)
        logger.info("document deleted id=%s", document_id)