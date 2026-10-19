"""
====================================================================
app/domain/entities.py — the core business object.
====================================================================

A "domain entity" is a plain Python object that represents a real
concept in our business. Here: a Document.

It is intentionally framework-free:
  - No FastAPI imports
  - No Pydantic
  - No database drivers

Why? Because the entity should outlive any web framework or DB.
If you change from FastAPI to Flask, or from Postgres to Mongo,
the Document entity stays exactly the same.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid


def _now() -> datetime:
    """Current UTC time. Wrapped so tests can mock it if needed."""
    return datetime.now(timezone.utc)


@dataclass
class Document:
    """
    The Document entity.

    `@dataclass` auto-generates __init__, __repr__, __eq__ for us.
    """

    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    # ---- factory ----------------------------------------------------
    @staticmethod
    def new(title: str, content: str) -> "Document":
        """Create a brand-new Document with a generated id and timestamps."""
        now = _now()
        return Document(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            created_at=now,
            updated_at=now,
        )

    # ---- mutations --------------------------------------------------
    def update(self, title: str | None = None, content: str | None = None) -> None:
        """
        Patch the document. Only fields that are not None get updated.
        Always bumps `updated_at`.
        """
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        self.updated_at = _now()