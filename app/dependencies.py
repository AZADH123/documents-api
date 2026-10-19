"""
====================================================================
app/dependencies.py — FastAPI dependency injection seams.
====================================================================

FastAPI has a feature called "Depends" that lets a route declare
what it needs (e.g. a service) and the framework figures out how
to build it. This file is the SINGLE place where we wire
"what the route needs" to "where it actually comes from".

If tomorrow you swap the in-memory repo for Postgres, you only
change this file (or app/main.py's lifespan) — the routes stay the same.
"""

from fastapi import Request

from app.repositories.base import DocumentRepository
from app.services.document_service import DocumentService


def get_document_repository(request: Request) -> DocumentRepository:
    """
    Return the repository stored on app.state during startup.
    `Request` is injected by FastAPI automatically.
    """
    return request.app.state.document_repository


def get_document_service(request: Request) -> DocumentService:
    """
    Build a fresh DocumentService for each request, injecting the
    repository it needs. This is the seam used by the controller.
    """
    repository = get_document_repository(request)
    return DocumentService(repository)