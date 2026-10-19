"""
====================================================================
app/core/middleware.py — cross-cutting request handling.
====================================================================

Middleware runs on EVERY request, before/after the route handler.
We use it for two things:
  1. Assign a unique X-Request-ID per request (great for debugging).
  2. Log the method, path, status code, and duration of each request.
"""

import logging
import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Adds an X-Request-ID to each request and logs the request line.
    """

    async def dispatch(self, request: Request, call_next):
        # Reuse a request ID if the client sent one, otherwise generate.
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        # Stash on request.state so handlers can read it if needed.
        request.state.request_id = request_id

        # Time the actual request handler.
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Echo the request ID back on the response.
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response


def add_middleware(app: FastAPI) -> None:
    """Register all middleware on the app."""
    app.add_middleware(RequestLoggingMiddleware)