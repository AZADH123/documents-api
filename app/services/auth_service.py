"""
====================================================================
app/services/auth_service.py — auth business rules.
====================================================================

Mirrors DocumentService, but for users + tokens:
  - register: hashes password, ensures email/username are unique,
              stores the user.
  - login:    verifies the password, mints a JWT.
  - get_user_by_id: looks a user up (used by get_current_user to
              turn a JWT subject back into a User).

The service has NO knowledge of HTTP. It can be reused from a CLI,
a background job, or tests.
"""

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.domain.entities import User
from app.domain.errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.repositories.base import UserRepository
from app.schemas.users import UserLogin, UserRegister, TokenResponse


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    # ---- register ---------------------------------------------------
    def register(self, payload: UserRegister) -> User:
        # Uniqueness checks (business rules belong here, not in the repo).
        if self.user_repository.find_by_email(payload.email) is not None:
            raise UserAlreadyExistsError(
                f"A user with email '{payload.email}' already exists"
            )
        if self.user_repository.find_by_username(payload.username) is not None:
            raise UserAlreadyExistsError(
                f"Username '{payload.username}' is already taken"
            )

        # NEVER store the plaintext password.
        hashed = hash_password(payload.password)
        user = User.new(
            username=payload.username,
            email=payload.email,
            hashed_password=hashed,
        )
        self.user_repository.add(user)
        return user

    # ---- login ------------------------------------------------------
    def login(self, payload: UserLogin) -> TokenResponse:
        user = self.user_repository.find_by_email(payload.email)
        # Use the SAME error for "no such email" and "wrong password"
        # so an attacker can't enumerate accounts by getting different
        # error messages.
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        token = create_access_token(subject=user.id)
        return TokenResponse(
            access_token=token,
            expires_in=settings.jwt_expire_minutes * 60,
        )

    # ---- me ---------------------------------------------------------
    def get_user_by_id(self, user_id: str) -> User:
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id '{user_id}' not found")
        return user