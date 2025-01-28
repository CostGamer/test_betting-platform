from typing import Optional

from fastapi import Request

from bet_maker.app.core.custom_exceptions import (
    EventNotFoundError,
    NoMoneyError,
    NotEnoughMoneyError,
)
from bet_maker.app.core.models.pydantic_models import Event, GetBet, PostBet, PostBetDTO
from bet_maker.app.core.schemas.repo_protocols import (
    BetRepoProtocol,
    UserRepoProtocol,
)
from bet_maker.app.core.schemas.service_protocols import (
    CommonServiceProtocol,
    GetEventsServiceProtocol,
)


class PostBetService:
    def __init__(
        self,
        bet_repo: BetRepoProtocol,
        event_service: GetEventsServiceProtocol,
        user_repo: UserRepoProtocol,
        common_service: CommonServiceProtocol,
    ) -> None:
        self._bet_repo = bet_repo
        self._event_service = event_service
        self._user_repo = user_repo
        self._common_service = common_service

    async def __call__(self, bet_data: PostBet, request: Request) -> GetBet:
        active_events = await self._event_service.get_active_events()

        event_data = self._find_event_by_name(bet_data.name, active_events)
        if not event_data:
            raise EventNotFoundError

        user_id = await self._common_service._get_user_id(request)

        balance = await self._user_repo.get_user_balance(user_id)
        if balance <= 0:
            raise NoMoneyError

        if bet_data.money_amount > balance:
            raise NotEnoughMoneyError

        await self._user_repo.change_user_balance(user_id, -bet_data.money_amount)

        bet_to_db = PostBetDTO(
            name=bet_data.name,
            money_amount=bet_data.money_amount,
            coefficient=event_data.coefficient,
            result=event_data.status,
            user_id=user_id,
        )
        bet = await self._bet_repo.make_bet(bet_to_db)
        return bet

    def _find_event_by_name(
        self, name: str, events_list: list[Event | None]
    ) -> Optional[Event]:
        return next(
            (event for event in events_list if event and event.name == name), None
        )


class GetBetsService:
    def __init__(
        self,
        bet_repo: BetRepoProtocol,
        common_service: CommonServiceProtocol,
    ) -> None:
        self._bet_repo = bet_repo
        self._common_service = common_service

    async def __call__(self, request: Request) -> list[GetBet]:
        user_id = await self._common_service._get_user_id(request)
        return await self._bet_repo.fetch_all_user_bets(user_id)


class GetActiveBetsService:
    def __init__(
        self,
        bet_repo: BetRepoProtocol,
        common_service: CommonServiceProtocol,
    ) -> None:
        self._bet_repo = bet_repo
        self._common_service = common_service

    async def __call__(self, request: Request) -> list[GetBet]:
        user_id = await self._common_service._get_user_id(request)
        return await self._bet_repo.fetch_all_user_bets(user_id)
