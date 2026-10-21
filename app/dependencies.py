"""
====================================================================
app/dependencies.py — FastAPI dependency-injection seams.
====================================================================

This is the SINGLE place where "what a route needs" is wired to
"where it actually comes from".
"""

import jwt
from fastapi import Request

from app.core.security import decode_access_token
from app.domain.entities import User
from app.domain.errors import InvalidTokenError
from app.repositories.base import DocumentRepository, UserRepository
from app.services.auth_service import AuthService
from app.services.document_service import DocumentService


# --------------------------------------------------------------------
# Documents
# --------------------------------------------------------------------
def get_document_repository(request: Request) -> DocumentRepository:
    return request.app.state.document_repository


def get_document_service(request: Request) -> DocumentService:
    return DocumentService(get_document_repository(request))


# --------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------
def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.user_repository


def get_auth_service(request: Request) -> AuthService:
    return AuthService(get_user_repository(request))


def get_current_user(request: Request) -> User:
    """
    Decode the Bearer JWT from the Authorization header and return
    the matching User. Used as a Depends() on protected routes.

    Raises InvalidTokenError → 401 if:
      - the header is missing or not "Bearer <token>"
      - the JWT signature is invalid
      - the JWT has expired
      - the subject (user id) is unknown
    """
    auth_service = get_auth_service(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise InvalidTokenError(
            "Missing Authorization header. Expected: 'Bearer <token>'"
        )

    token = auth_header[len("Bearer "):].strip()

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token.")

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError("Token is missing subject.")

    # Raises UserNotFoundError if the id no longer exists.
    return auth_service.get_user_by_id(user_id)