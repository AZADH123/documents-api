"""
====================================================================
app/core/exception_handlers.py — turn domain errors into HTTP.
====================================================================
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.errors import (
    AuthError,
    DocumentError,
    DocumentNotFoundError,
    DuplicateDocumentError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.schemas.errors import ErrorResponse


def _envelope(exc, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
        ).model_dump(),
    )


def add_exception_handlers(app: FastAPI) -> None:
    # ---- Document errors ----
    @app.exception_handler(DocumentNotFoundError)
    async def _not_found(_: Request, exc: DocumentNotFoundError):
        return _envelope(exc, status_code=404)

    @app.exception_handler(DuplicateDocumentError)
    async def _duplicate(_: Request, exc: DuplicateDocumentError):
        return _envelope(exc, status_code=409)

    @app.exception_handler(DocumentError)
    async def _base_doc(_: Request, exc: DocumentError):
        return _envelope(exc, status_code=400)

    # ---- Auth errors ----
    @app.exception_handler(InvalidCredentialsError)
    async def _bad_creds(_: Request, exc: InvalidCredentialsError):
        return _envelope(exc, status_code=401)

    @app.exception_handler(InvalidTokenError)
    async def _bad_token(_: Request, exc: InvalidTokenError):
        return _envelope(exc, status_code=401)

    @app.exception_handler(UserAlreadyExistsError)
    async def _dup_user(_: Request, exc: UserAlreadyExistsError):
        return _envelope(exc, status_code=409)

    @app.exception_handler(UserNotFoundError)
    async def _user_not_found(_: Request, exc: UserNotFoundError):
        return _envelope(exc, status_code=404)

    @app.exception_handler(AuthError)
    async def _base_auth(_: Request, exc: AuthError):
        return _envelope(exc, status_code=400)