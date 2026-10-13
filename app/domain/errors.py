class DomainError(Exception):
    """Base class for business-rule violations."""

    code: str = "DOMAIN_ERROR"


class DocumentNotFoundError(DomainError):
    code: str = "DOCUMENT_NOT_FOUND"

    def __init__(self, document_id: str) -> None:
        self.document_id = document_id
        super().__init__(f"Document '{document_id}' not found")