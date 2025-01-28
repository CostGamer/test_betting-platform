from fastapi import APIRouter, Depends, Query, Request

from bet_maker.app.api.dependencies import (
    get_balance_service,
    get_user_info_service,
)
from bet_maker.app.api.exception_responses.responses import (
    get_balance_top_up_responses,
    get_balance_withdraw_responses,
    get_user_info_responses,
)
from bet_maker.app.core.models.pydantic_models import UserModel
from bet_maker.app.core.schemas.service_protocols import (
    BalanceServiceProtocol,
    GetUserInfoServiceProtocol,
)

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    "/",
    response_model=UserModel,
    responses=get_user_info_responses,
    description="Get user info",
)
async def get_user_info(
    request: Request,
    user_service: GetUserInfoServiceProtocol = Depends(get_user_info_service),
) -> UserModel:
    return await user_service(request)


@user_router.put(
    "/balance/top_up",
    response_model=float,
    responses=get_balance_top_up_responses,
    description="Top up the user balance",
)
async def top_up_user_balance(
    request: Request,
    amount: float = Query(gt=0),
    user_service: BalanceServiceProtocol = Depends(get_balance_service),
) -> float:
    return await user_service.top_up(amount, request)


@user_router.put(
    "/balance/withdraw",
    response_model=float,
    responses=get_balance_withdraw_responses,
    description="Withdraw the user balance",
)
async def withdraw_user_balance(
    request: Request,
    amount: float = Query(gt=0),
    user_service: BalanceServiceProtocol = Depends(get_balance_service),
) -> float:
    return await user_service.withdraw(amount, request)
