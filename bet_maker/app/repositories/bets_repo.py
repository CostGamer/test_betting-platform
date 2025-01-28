from pydantic import UUID4
from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.app.core.models.pydantic_models import GetBet, PostBetDTO
from bet_maker.app.core.models.sqlalchemy_models import Bets, Users


class BetRepo:
    def __init__(self, con: AsyncSession):
        self._con = con

    async def make_bet(self, bet_data: PostBetDTO) -> GetBet:
        query = (
            insert(Bets)
            .values(
                name=bet_data.name,
                coefficient=bet_data.coefficient,
                money_amount=bet_data.money_amount,
                result=bet_data.result,
                user_id=bet_data.user_id,
            )
            .returning(Bets)
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return GetBet.model_validate(query_res)

    async def fetch_active_bet(self, user_id: UUID4) -> list[GetBet]:
        query = (
            select(Bets).join(Users).where(and_(Users.id == user_id, Bets.result == 1))
        )

        query_res = (await self._con.execute(query)).scalars().all()
        return [GetBet.model_validate(event) for event in query_res]

    async def fetch_all_user_bets(self, user_id: UUID4) -> list[GetBet]:
        query = select(Bets).join(Users).where(Users.id == user_id)

        query_res = (await self._con.execute(query)).scalars().all()
        return [GetBet.model_validate(event) for event in query_res]
