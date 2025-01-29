from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from shared.configs.database import DatabaseConnection
from shared.configs.settings import Settings


class DatabaseConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_database(self, settings: Settings) -> DatabaseConnection:
        return DatabaseConnection(settings)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(
        self, database: DatabaseConnection
    ) -> AsyncIterator[AsyncSession]:
        async with database.get_session() as session:
            yield session
