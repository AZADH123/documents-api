"""
====================================================================
app/domain/errors.py — domain-level exceptions.
====================================================================

The service layer raises these. They have NO knowledge of HTTP.
The exception_handlers.py file translates them into HTTP responses.

Why use exceptions instead of returning None / Result objects?
Because raising an exception forces every caller to handle it
(or let it bubble up) — you can't silently ignore a missing document.
"""


class DocumentError(Exception):
    """Base class for all document-related domain errors."""

    message: str = "Document error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class DocumentNotFoundError(DocumentError):
    """Raised when a document id doesn't exist."""

    message = "Document not found"


class DuplicateDocumentError(DocumentError):
    """Raised when a document already exists with the same key."""

    message = "Document already exists"