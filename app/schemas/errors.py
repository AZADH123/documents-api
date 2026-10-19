"""
====================================================================
app/schemas/errors.py — error response DTO.
====================================================================

The single shape used for all error responses, e.g.:

    {
      "error": "DocumentNotFoundError",
      "message": "Document with id 'abc' not found"
    }
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str    # the exception class name (machine-readable)
    message: str  # human-readable explanation