"""
====================================================================
app/repositories/in_memory.py — dict-backed repositories.
====================================================================
"""

from app.domain.entities import Document, User
from app.domain.errors import DuplicateDocumentError


# --------------------------------------------------------------------
# Document repository
# --------------------------------------------------------------------
class InMemoryDocumentRepository:
    def __init__(self) -> None:
        self._store: dict[str, Document] = {}

    def add(self, document: Document) -> None:
        if document.id in self._store:
            raise DuplicateDocumentError(
                f"Document with id '{document.id}' already exists"
            )
        self._store[document.id] = document

    def get(self, document_id: str) -> Document | None:
        return self._store.get(document_id)

    def list_all(self) -> list[Document]:
        return list(self._store.values())

    def delete(self, document_id: str) -> bool:
        if document_id in self._store:
            del self._store[document_id]
            return True
        return False

    def exists(self, document_id: str) -> bool:
        return document_id in self._store


# --------------------------------------------------------------------
# User repository
# --------------------------------------------------------------------
class InMemoryUserRepository:
    """
    Stores users in a dict, with two extra indexes (by email and by
    username) so login/registration lookups are O(1).
    """

    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._by_email: dict[str, str] = {}      # email -> user_id
        self._by_username: dict[str, str] = {}   # username -> user_id

    def add(self, user: User) -> None:
        self._by_id[user.id] = user
        self._by_email[user.email] = user.id
        self._by_username[user.username] = user.id

    def get(self, user_id: str) -> User | None:
        return self._by_id.get(user_id)

    def find_by_email(self, email: str) -> User | None:
        user_id = self._by_email.get(email)
        return self._by_id.get(user_id) if user_id else None

    def find_by_username(self, username: str) -> User | None:
        user_id = self._by_username.get(username)
        return self._by_id.get(user_id) if user_id else None