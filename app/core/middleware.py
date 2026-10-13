import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("app.access")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request with latency and a correlation id, echoed back
    as X-Request-ID so a request can be traced end-to-end through logs."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        started = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.info(
            "%s %s -> %s (%.1fms) request_id=%s",
            request.method, request.url.path, response.status_code, elapsed_ms, request_id,
        )
        response.headers["X-Request-ID"] = request_id
        return response