import asyncio
from logging import getLogger
from uuid import UUID

from bet_maker.app.core.models.pydantic_models import ActiveBets
from bet_maker.app.core.schemas.repo_protocols import BetRepoProtocol, UserRepoProtocol
from bet_maker.app.core.schemas.service_protocols import GetEventsServiceProtocol

logger = getLogger(__name__)


class BackgroundTasksService:
    def __init__(
        self,
        bet_repo: BetRepoProtocol,
        event_service: GetEventsServiceProtocol,
        user_repo: UserRepoProtocol,
    ) -> None:
        self._bet_repo = bet_repo
        self._event_service = event_service
        self._user_repo = user_repo

    async def check_bet_status(self) -> None:
        all_active_bets = await self._bet_repo.fetch_all_active_bets()
        all_events = await self._event_service.get_all_events()

        active_bets_dict = {bet.event_id: bet for bet in all_active_bets}

        for event in all_events:
            assert event is not None
            event_id = UUID(event.event_id, version=4)
            bet = active_bets_dict.get(event_id)

            if bet:
                result = event.status
                await self._process_bet(bet, result)

    async def _process_bet(self, bet: ActiveBets, result: int) -> None:
        changed_bets = await self._bet_repo.change_bet_status(
            result=result, name=bet.name, event_id=bet.event_id
        )

        for finished_bet in changed_bets:
            if finished_bet.result == 2:
                win_amount = round(
                    finished_bet.coefficient * finished_bet.money_amount, 2
                )
                await self._user_repo.change_user_balance(
                    finished_bet.user_id, win_amount
                )

    async def monitor_periodically(self, interval: int = 30) -> None:
        while True:
            try:
                await self.check_bet_status()
            except Exception as e:
                logger.warning(f"Error while checking bet status: {e}")
            await asyncio.sleep(interval)
