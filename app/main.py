"""
====================================================================
app/main.py — the application factory.
====================================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import add_middleware
from app.repositories.in_memory import InMemoryDocumentRepository, InMemoryUserRepository
from app.routers import auth, documents, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----- startup -----
    setup_logging()
    # Wire up repositories. Swap these for Postgres-backed repos later
    # without touching any other file.
    app.state.document_repository = InMemoryDocumentRepository()
    app.state.user_repository = InMemoryUserRepository()

    yield  # app runs while we yield

    # ----- shutdown (nothing to clean up) -----


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    add_middleware(app)
    add_exception_handlers(app)

    # Routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(documents.router)

    return app


app = create_app()