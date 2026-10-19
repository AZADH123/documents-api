"""
====================================================================
index.py — the entry point of the application.
====================================================================

You start the server by running:
    python index.py

This file does only ONE thing: it tells Uvicorn (the web server)
to load our FastAPI app and start listening for HTTP requests.
"""

import uvicorn

# Import our settings (loaded from .env) so we know host/port/debug.
from app.core.config import settings


if __name__ == "__main__":
    # uvicorn.run(...) starts the ASGI web server.
    #
    # Arguments:
    #   "app.main:app" — Python path to the FastAPI instance:
    #                    file `app/main.py`, variable `app`.
    #   host           — network interface to bind ("0.0.0.0" = all).
    #   port           — TCP port (8000 by default).
    #   reload         — auto-restart on file changes (dev only).
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )