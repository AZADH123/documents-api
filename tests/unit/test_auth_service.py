"""
====================================================================
tests/unit/test_auth_service.py — unit tests for AuthService.
====================================================================
"""

import pytest

from app.domain.errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.repositories.in_memory import InMemoryUserRepository
from app.schemas.users import UserLogin, UserRegister
from app.services.auth_service import AuthService


def _make_service() -> AuthService:
    return AuthService(InMemoryUserRepository())


# ---------- register ------------------------------------------------
def test_register_creates_user_with_hashed_password():
    service = _make_service()
    user = service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    assert user.id
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    # CRITICAL: the stored password must NOT be the plaintext one
    assert user.hashed_password != "secret123"
    assert len(user.hashed_password) > 0


def test_register_rejects_duplicate_email():
    service = _make_service()
    service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    with pytest.raises(UserAlreadyExistsError):
        service.register(
            UserRegister(username="alice2", email="alice@example.com", password="secret456")
        )


def test_register_rejects_duplicate_username():
    service = _make_service()
    service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    with pytest.raises(UserAlreadyExistsError):
        service.register(
            UserRegister(username="alice", email="other@example.com", password="secret456")
        )


# ---------- login ---------------------------------------------------
def test_login_returns_token_for_valid_credentials():
    service = _make_service()
    service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    token = service.login(
        UserLogin(email="alice@example.com", password="secret123")
    )

    assert token.access_token
    assert token.token_type == "bearer"
    assert token.expires_in > 0


def test_login_rejects_wrong_password():
    service = _make_service()
    service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    with pytest.raises(InvalidCredentialsError):
        service.login(UserLogin(email="alice@example.com", password="WRONG"))


def test_login_rejects_unknown_email():
    service = _make_service()
    with pytest.raises(InvalidCredentialsError):
        service.login(UserLogin(email="ghost@example.com", password="x"))


# ---------- get_user_by_id -----------------------------------------
def test_get_user_by_id_returns_user():
    service = _make_service()
    user = service.register(
        UserRegister(username="alice", email="alice@example.com", password="secret123")
    )

    fetched = service.get_user_by_id(user.id)
    assert fetched.id == user.id


def test_get_user_by_id_missing_raises():
    service = _make_service()
    with pytest.raises(UserNotFoundError):
        service.get_user_by_id("does-not-exist")