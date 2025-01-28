from pydantic import UUID4
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.app.core.models.pydantic_models import UserModel
from bet_maker.app.core.models.sqlalchemy_models import Users


class UserRepo:
    def __init__(self, con: AsyncSession):
        self._con = con

    async def get_user_balance(self, user_id: UUID4) -> float:
        query = select(Users.balance).where(Users.id == user_id)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def change_user_balance(self, user_id: UUID4, amount: float) -> float:
        query = (
            update(Users)
            .where(Users.id == user_id)
            .values(balance=Users.balance + amount)
            .returning(Users.balance)
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_user_info(
        self,
        user_id: UUID4,
    ) -> UserModel:
        query = select(Users).where(Users.id == user_id)
        query_res = (await self._con.execute(query)).scalar_one()
        return UserModel.model_validate(query_res)
