"""
====================================================================
app/core/security.py — password hashing + JWT helpers.
====================================================================

Two concerns, both auth-related, kept here so the service layer
stays clean:

  1. Password hashing  — we never store plaintext passwords.
     We use bcrypt (slow on purpose, so brute-forcing is hard).

  2. JWT creation/verification — JWTs are signed tokens that prove
     "the server issued this". They contain a subject (user id),
     an issued-at time, and an expiry. They are NOT encrypted —
     anyone can read them, but no one can forge them without the
     secret (JWT_SECRET in your .env).
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


# --------------------------------------------------------------------
# Password hashing
# --------------------------------------------------------------------
def hash_password(plain: str) -> str:
    """
    Hash a plaintext password using bcrypt. Returns a string safe to
    store in a DB. The salt is embedded in the hash itself, so we
    don't need to store it separately.
    """
    # bcrypt works on bytes, so encode the string first.
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Check that `plain` matches the previously-computed `hashed`.
    Returns True/False — never raises on a mismatch.
    """
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        # Malformed hash — treat as a failed verification.
        return False


# --------------------------------------------------------------------
# JWT
# --------------------------------------------------------------------
def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    Build a signed JWT for the given subject (typically a user id).

    The token encodes:
      - "sub": the subject (user id)
      - "iat": issued-at time
      - "exp": expiry time
    """
    minutes = expires_minutes if expires_minutes is not None else settings.jwt_expire_minutes
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """
    Verify the signature AND expiry of a JWT, returning its payload.

    Raises jwt.ExpiredSignatureError if expired.
    Raises jwt.InvalidTokenError  if signature/format is bad.
    The caller (get_current_user) turns these into InvalidTokenError.
    """
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )