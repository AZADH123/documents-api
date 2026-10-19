"""
====================================================================
app/routers/health.py — liveness & readiness probes.
====================================================================

Two tiny endpoints that orchestrators (Kubernetes, Docker, load
balancers) use to decide whether the app is alive and ready.

  /healthz — "is the process running?"  (always 200 if up)
  /readyz  — "is the app ready to serve traffic?"
             (here: same as healthz, but in real life this is
              where you'd check the DB connection, etc.)
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@router.get("/readyz")
def readyz() -> dict:
    return {"status": "ready"}