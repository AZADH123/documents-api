"""
====================================================================
app/domain/entities.py — domain objects (framework-free).
====================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid


def _now() -> datetime:
    return datetime.now(timezone.utc)


# --------------------------------------------------------------------
# Document
# --------------------------------------------------------------------
@dataclass
class Document:
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def new(title: str, content: str) -> "Document":
        now = _now()
        return Document(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            created_at=now,
            updated_at=now,
        )

    def update(self, title: str | None = None, content: str | None = None) -> None:
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        self.updated_at = _now()


# --------------------------------------------------------------------
# User
# --------------------------------------------------------------------
@dataclass
class User:
    """
    A registered user. Stores a HASHED password — never the plaintext.

    Like Document, this is plain Python with no FastAPI / DB imports,
    so it can be reused from anywhere (CLI, tests, background jobs).
    """

    id: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime

    @staticmethod
    def new(username: str, email: str, hashed_password: str) -> "User":
        return User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            hashed_password=hashed_password,
            created_at=_now(),
        )