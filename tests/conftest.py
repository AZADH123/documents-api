import pytest
from fastapi.testclient import TestClient

from app.controllers.documents_controller import DocumentsController
from app.main import create_app
from app.repositories.in_memory import InMemoryDocumentRepository
from app.services.document_service import DocumentService


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    with TestClient(app) as test_client:   # context manager runs lifespan
        # swap in a fresh store so every test is isolated
        repository = InMemoryDocumentRepository()
        app.state.document_repository = repository
        app.state.document_service = DocumentService(repository)
        app.state.documents_controller = DocumentsController(app.state.document_service)
        yield test_client