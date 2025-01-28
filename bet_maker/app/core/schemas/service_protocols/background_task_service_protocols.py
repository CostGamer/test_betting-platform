from typing import Protocol

from bet_maker.app.core.models.pydantic_models import ActiveBets


class BackgroundTasksServiceProtocol(Protocol):
    async def check_bet_status(self) -> None:
        """Check the status of all active bets and update their results accordingly"""
        pass

    async def _process_bet(self, bet: ActiveBets) -> None:
        """Process the status of a single active bet and update user balances if necessary"""
        pass

    async def monitor_periodically(self, interval: int = ...) -> None:
        """Infinity monitoring"""
        pass
