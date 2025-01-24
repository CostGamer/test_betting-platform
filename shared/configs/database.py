from collections.abc import AsyncIterator, Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.configs.settings import PostgresSettings


def get_session(
    pgdb_settings: PostgresSettings,
) -> Callable[[], AsyncIterator[AsyncSession]]:
    """Creates a database session factory for interacting with the database.

    This function configures and returns a session factory that will provide an asynchronous session
    to interact with the database. The session factory is designed to handle transactions, automatically
    committing changes and rolling back in case of errors.

    Args:
        db_settings (PostgresSettings): Configuration settings for the database connection, including
                                         the URI, pool size, and overflow settings.

    Returns:
        Callable[[], AsyncIterator[AsyncSession]]: A function that, when called, will return an asynchronous
                                                   iterator yielding a session object (`AsyncSession`).
    """
    async_engine = create_async_engine(
        pgdb_settings.db_uri,
        echo=False,
        pool_size=pgdb_settings.pool_size,
        max_overflow=pgdb_settings.max_overflow,
    )
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    async def recieve_session() -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as err:
                await session.rollback()
                raise err

    return recieve_session
