"""
====================================================================
app/core/exception_handlers.py — turn domain errors into HTTP.
====================================================================

The service layer raises DOMAIN exceptions (e.g. DocumentNotFoundError)
because it doesn't know it's being called from HTTP. This file is
the bridge: it catches those exceptions and converts them into
JSON HTTP responses with a consistent error envelope.

Example error response:
    {
      "error": "DocumentNotFoundError",
      "message": "Document with id 'abc' not found"
    }
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.errors import (
    DocumentError,
    DocumentNotFoundError,
    DuplicateDocumentError,
)
from app.schemas.errors import ErrorResponse


def _envelope(exc: DocumentError, status_code: int) -> JSONResponse:
    """Build a JSONResponse from a domain error."""
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
        ).model_dump(),
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the app."""

    @app.exception_handler(DocumentNotFoundError)
    async def _not_found(_: Request, exc: DocumentNotFoundError):
        return _envelope(exc, status_code=404)

    @app.exception_handler(DuplicateDocumentError)
    async def _duplicate(_: Request, exc: DuplicateDocumentError):
        return _envelope(exc, status_code=409)

    @app.exception_handler(DocumentError)
    async def _base_error(_: Request, exc: DocumentError):
        # Catch-all for any other DocumentError subclass -> 400 Bad Request.
        return _envelope(exc, status_code=400)