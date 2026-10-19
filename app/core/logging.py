"""
====================================================================
app/core/logging.py — logging bootstrap.
====================================================================

Centralized logging setup so every part of the app logs in the
same format. We call setup_logging() once at startup (see main.py).
"""

import logging
import sys


def setup_logging() -> None:
    """Configure the root logger with a consistent format."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    root = logging.getLogger()
    # Clear any handlers that libraries might have added (e.g. uvicorn)
    # so we have full control over the format.
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)