from fastapi import APIRouter, Depends, Request

from bet_maker.app.api.dependencies import (
    get_active_bets_service,
    get_bets_service,
    get_post_bet_service,
)
from bet_maker.app.api.exception_responses.responses import (
    get_all_active_bets_responses,
    get_all_bets_responses,
    post_bet_responses,
)
from bet_maker.app.core.models.pydantic_models import GetBet, PostBet
from bet_maker.app.core.schemas.service_protocols import (
    GetActiveBetsServiceProtocol,
    GetBetsServiceProtocol,
    PostBetServiceProtocol,
)

bets_router = APIRouter(prefix="/bets", tags=["bets"])


@bets_router.post(
    "/bet",
    response_model=GetBet,
    responses=post_bet_responses,
    description="Post handler for betting",
)
async def make_bet(
    bet_data: PostBet,
    request: Request,
    bet_service: PostBetServiceProtocol = Depends(get_post_bet_service),
) -> GetBet:
    return await bet_service(bet_data, request)


@bets_router.get(
    "/",
    response_model=list[GetBet],
    responses=get_all_bets_responses,
    description="Fetch history of user's bets",
)
async def get_all_bets(
    request: Request,
    bet_service: GetBetsServiceProtocol = Depends(get_bets_service),
) -> list[GetBet]:
    return await bet_service(request)


@bets_router.get(
    "/active",
    response_model=list[GetBet],
    responses=get_all_active_bets_responses,
    description="Fetch active of user's bets",
)
async def get_all_active_bets(
    request: Request,
    bet_service: GetActiveBetsServiceProtocol = Depends(get_active_bets_service),
) -> list[GetBet]:
    return await bet_service(request)
