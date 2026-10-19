"""
====================================================================
app/main.py — the application factory.
====================================================================

This file builds the FastAPI app:
  1. Wires up the lifespan (startup/shutdown hooks).
  2. Registers middleware (request logging, request IDs).
  3. Registers exception handlers (turn domain errors into HTTP).
  4. Includes all routers (health + documents).

Other code never imports `app` directly except Uvicorn (via index.py)
and the test client (via create_app()).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import add_middleware
from app.core.exception_handlers import add_exception_handlers
from app.repositories.in_memory import InMemoryDocumentRepository
from app.routers import documents, health


# --------------------------------------------------------------------
# Lifespan: runs once on startup and once on shutdown.
# We create our repository here and stash it on `app.state` so the
# dependency-injection seams (see app/dependencies.py) can find it.
# --------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ----- startup -----
    setup_logging()
    # Today we use an in-memory dict. Next week we can swap this for
    # a Postgres repository without touching any other file.
    app.state.document_repository = InMemoryDocumentRepository()

    yield  # the app runs while we yield

    # ----- shutdown (nothing to clean up right now) -----


# --------------------------------------------------------------------
# Application factory.
# Encapsulating creation in a function makes the app easy to test:
# tests can call create_app() and override app.state if they want.
# --------------------------------------------------------------------
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Cross-cutting concerns (apply to every request):
    add_middleware(app)
    add_exception_handlers(app)

    # Routers (the actual endpoints):
    app.include_router(health.router)
    app.include_router(documents.router)

    return app


# This is what Uvicorn imports when you run `python index.py`.
app = create_app()