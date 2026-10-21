"""
====================================================================
app/controllers/auth_controller.py — HTTP ↔ AuthService adapter.
====================================================================
"""

from fastapi import Depends

from app.dependencies import get_auth_service
from app.domain.entities import User
from app.schemas.users import UserLogin, UserRegister, UserResponse, TokenResponse
from app.services.auth_service import AuthService


class AuthController:
    """
    Same thin-adapter pattern as DocumentsController:
    DTOs in → service call → entity out → response DTO.
    """

    def __init__(
        self,
        service: AuthService = Depends(get_auth_service),
    ) -> None:
        self.service = service

    # ---- register ---------------------------------------------------
    def register(self, payload: UserRegister) -> UserResponse:
        user = self.service.register(payload)
        return UserResponse.from_entity(user)

    # ---- login ------------------------------------------------------
    def login(self, payload: UserLogin) -> TokenResponse:
        return self.service.login(payload)

    # ---- me (returns the already-authenticated user) ----------------
    @staticmethod
    def me(current_user: User) -> UserResponse:
        return UserResponse.from_entity(current_user)