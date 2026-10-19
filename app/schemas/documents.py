"""
====================================================================
app/schemas/documents.py — request/response DTOs (Pydantic).
====================================================================

DTO = Data Transfer Object. These are the shapes that cross the
HTTP boundary. Think of them like Zod schemas in TypeScript:
  - FastAPI uses them to validate the incoming request body.
  - FastAPI uses them to serialize the outgoing response body.
  - They are NOT the same as the domain entity — the entity lives
    inside the app, the schema is what the outside world sees.

Why separate schema vs entity? Because the API might expose fields
the entity doesn't have (or hide fields the entity does have).
"""

from datetime import datetime

from pydantic import BaseModel, Field


# --------------------------------------------------------------------
# Request DTOs
# --------------------------------------------------------------------
class DocumentCreate(BaseModel):
    """Body of POST /documents/."""

    # Field(...) means "required". min/max length is enforced by FastAPI.
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field("", max_length=10000)


class DocumentUpdate(BaseModel):
    """Body of PUT /documents/{id}. All fields optional (partial update)."""

    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, max_length=10000)


# --------------------------------------------------------------------
# Response DTO
# --------------------------------------------------------------------
class DocumentResponse(BaseModel):
    """Body returned by GET/POST/PUT /documents/..."""

    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, doc) -> "DocumentResponse":
        """Convert a domain entity into a response DTO."""
        return cls(
            id=doc.id,
            title=doc.title,
            content=doc.content,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )