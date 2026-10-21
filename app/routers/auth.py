"""
====================================================================
app/routers/auth.py — auth route table.
====================================================================

Three endpoints under /auth:
  POST /auth/register   — create a user account
  POST /auth/login      — exchange email+password for a JWT
  GET  /auth/me         — return the currently authenticated user
                          (requires Authorization: Bearer <token>)
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers.auth_controller import AuthController
from app.dependencies import get_current_user
from app.domain.entities import User
from app.schemas.users import UserLogin, UserRegister, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# A reusable type alias: any route parameter annotated with this
# automatically triggers JWT verification via get_current_user.
CurrentUser = Annotated[User, Depends(get_current_user)]


# --------------------------------------------------------------------
# POST /auth/register
# --------------------------------------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: UserRegister,controller: AuthController = Depends(),
) -> UserResponse:
    return controller.register(payload)


# --------------------------------------------------------------------
# POST /auth/login
# --------------------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
def login(
    payload: UserLogin,
    controller: AuthController = Depends(),
) -> TokenResponse:
    return controller.login(payload)


# --------------------------------------------------------------------
# GET /auth/me  (PROTECTED)
# --------------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
def me(
    current_user: CurrentUser,
    controller: AuthController = Depends(),
) -> UserResponse:
    # current_user is already the authenticated User entity —
    # the dependency did all the JWT work for us.
    return controller.me(current_user)