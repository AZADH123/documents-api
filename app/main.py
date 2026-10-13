import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings, get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.controllers.documents_controller import DocumentsController
from app.repositories.in_memory import InMemoryDocumentRepository
from app.routers import documents, health
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the object graph once at startup. Next week's persistence
    switch happens HERE — one line — nothing else changes."""
    repository = InMemoryDocumentRepository()
    service = DocumentService(repository)
    controller = DocumentsController(service)

    app.state.document_repository = repository
    app.state.document_service = service
    app.state.documents_controller = controller

    settings = get_settings()
    logger.info("startup complete environment=%s", settings.environment)
    yield
    # Later: close DB connection pools, flush buffers, etc.
    logger.info("shutdown complete")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
        # For a hardened prod deployment you may want docs_url=None here.
    )

    register_exception_handlers(app)
    app.add_middleware(RequestLoggingMiddleware)

    if settings.cors_origins:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(health.router)
    app.include_router(documents.router, prefix=settings.api_v1_prefix)
    return app


app = create_app()