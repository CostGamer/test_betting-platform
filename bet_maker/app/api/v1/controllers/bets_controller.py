from fastapi import APIRouter, Depends, Request

from bet_maker.app.api.dependencies import get_post_bet_service
from bet_maker.app.api.exception_responses.responses import post_bet_responses
from bet_maker.app.core.models.pydantic_models import GetBet, PostBet
from bet_maker.app.core.schemas.service_protocols import PostBetServiceProtocol

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
