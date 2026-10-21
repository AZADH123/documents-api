"""
====================================================================
app/repositories/base.py — repository contracts (Protocols).
====================================================================
"""

from typing import Protocol

from app.domain.entities import Document, User


# --------------------------------------------------------------------
# Documents
# --------------------------------------------------------------------
class DocumentRepository(Protocol):
    def add(self, document: Document) -> None: ...
    def get(self, document_id: str) -> Document | None: ...
    def list_all(self) -> list[Document]: ...
    def delete(self, document_id: str) -> bool: ...
    def exists(self, document_id: str) -> bool: ...


# --------------------------------------------------------------------
# Users
# --------------------------------------------------------------------
class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get(self, user_id: str) -> User | None: ...
    def find_by_email(self, email: str) -> User | None: ...
    def find_by_username(self, username: str) -> User | None: ...