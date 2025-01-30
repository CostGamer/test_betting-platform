from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.configs import all_settings

async_engine = create_async_engine(
    all_settings.database.db_uri,
    echo=False,
    pool_size=all_settings.database.pool_size,
    max_overflow=all_settings.database.max_overflow,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            raise err
