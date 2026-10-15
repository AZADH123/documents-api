from app.domain.entities import Document


class InMemoryDocumentRepository:
    """dict-backed implementation (Python's Map). Methods are async from day
    one so the database-backed replacement is a drop-in."""

    def __init__(self) -> None:
        self._documents: dict[str, Document] = {}

    async def add(self, document: Document) -> Document:
        self._documents[document.id] = document
        return document

    async def get(self, document_id: str) -> Document | None:
        return self._documents.get(document_id)

    async def list_all(self) -> list[Document]:
        return list(self._documents.values())   # dict preserves insertion order

    async def save(self, document: Document) -> None:
        self._documents[document.id] = document

    async def delete(self, document_id: str) -> bool:
        return self._documents.pop(document_id, None) is not None