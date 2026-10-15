from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz", summary="Liveness probe")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz", summary="Readiness probe")
async def readiness() -> dict[str, str]:
    # When the real store lands, ping it here and 503 on failure.
    return {"status": "ready"}