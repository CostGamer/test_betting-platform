from fastapi import APIRouter, Depends
from pydantic import UUID4

from bet_maker.app.api.dependencies import (
    get_login_service,
    get_register_service,
    get_reissue_service,
)
from bet_maker.app.api.exception_responses.responses import (
    get_token_reissue_responses,
    get_user_login_responses,
    get_user_register_responses,
)
from bet_maker.app.core.models.pydantic_models import JWTTokenInfo, RegisterUser
from bet_maker.app.core.schemas.service_protocols import (
    LoginAuthServiceProtocol,
    RegisterAuthServiceProtocol,
    ReissueTokenServiceProtocol,
)

auth_router = APIRouter(prefix="/auth", tags=["jwt"])


@auth_router.post(
    "/register",
    response_model=UUID4,
    responses=get_user_register_responses,
    description="Registration for users",
)
async def register_user(
    user_data: RegisterUser,
    register_service: RegisterAuthServiceProtocol = Depends(get_register_service),
) -> UUID4:
    return await register_service(user_data)


@auth_router.get(
    "/login",
    response_model=JWTTokenInfo,
    responses=get_user_login_responses,
    description="Login into your account",
)
async def login_user(
    email: str,
    password: str,
    login_service: LoginAuthServiceProtocol = Depends(get_login_service),
) -> JWTTokenInfo:
    return await login_service(email, password)


@auth_router.post(
    "/token/reissue",
    response_model=JWTTokenInfo,
    responses=get_token_reissue_responses,
    description="Generate new access JWT by refresh",
)
async def get_new_access(
    token: str,
    login_service: ReissueTokenServiceProtocol = Depends(get_reissue_service),
) -> JWTTokenInfo:
    return await login_service(token)
