from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Document:
    """Domain entity. No Pydantic, no FastAPI — services speak in these,
    controllers translate to/from DTOs at the edges."""

    id: str
    title: str
    content: str
    created_at: datetime