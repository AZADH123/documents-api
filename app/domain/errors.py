"""
====================================================================
app/domain/errors.py — domain-level exceptions.
====================================================================
"""


# --------------------------------------------------------------------
# Document errors
# --------------------------------------------------------------------
class DocumentError(Exception):
    message: str = "Document error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class DocumentNotFoundError(DocumentError):
    message = "Document not found"


class DuplicateDocumentError(DocumentError):
    message = "Document already exists"


# --------------------------------------------------------------------
# Auth / user errors
# --------------------------------------------------------------------
class AuthError(Exception):
    """Base class for all auth-related domain errors."""

    message: str = "Auth error"

    def __init__(self, message: str | None = None):
        self.message = message or self.message
        super().__init__(self.message)


class UserNotFoundError(AuthError):
    message = "User not found"


class UserAlreadyExistsError(AuthError):
    message = "User already exists"


class InvalidCredentialsError(AuthError):
    """Wrong email/password combination."""

    message = "Invalid credentials"


class InvalidTokenError(AuthError):
    """Missing, malformed, or expired JWT."""

    message = "Invalid or missing authentication token"