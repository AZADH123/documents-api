"""
====================================================================
app/schemas/users.py — request/response DTOs for auth.
====================================================================
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# --------------------------------------------------------------------
# Request DTOs
# --------------------------------------------------------------------
class UserRegister(BaseModel):
    """Body of POST /auth/register."""

    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr  # Pydantic validates the email format
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    """Body of POST /auth/login."""

    email: EmailStr
    password: str = Field(..., min_length=1)


# --------------------------------------------------------------------
# Response DTOs
# --------------------------------------------------------------------
class UserResponse(BaseModel):
    """
    Public representation of a user. Never includes the password
    (not even the hash) — that field must never leave the server.
    """

    id: str
    username: str
    email: str
    created_at: datetime

    @classmethod
    def from_entity(cls, user) -> "UserResponse":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
        )


class TokenResponse(BaseModel):
    """Returned by POST /auth/login."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until expiry