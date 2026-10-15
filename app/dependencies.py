from fastapi import Request

from app.controllers.documents_controller import DocumentsController
from app.repositories.base import DocumentRepository
from app.services.document_service import DocumentService


# Dependencies read from app.state, which the lifespan builds once at startup.
# Tests swap these via app.state (or dependency_overrides) for isolation.

def get_document_repository(request: Request) -> DocumentRepository:
    return request.app.state.document_repository


def get_document_service(request: Request) -> DocumentService:
    return request.app.state.document_service


def get_documents_controller(request: Request) -> DocumentsController:
    return request.app.state.documents_controller