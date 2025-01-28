import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from email_validator.exceptions_types import EmailNotValidError
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from jwt.exceptions import InvalidTokenError
from redis.asyncio import Redis

from bet_maker.app.api.dependencies import get_jwt_service
from bet_maker.app.api.exception_responses.exceptions import (
    email_not_valid_error,
    event_not_found_error,
    invalid_jwt_error,
    invalid_username_password_error,
    no_money_error,
    not_enough_money_error,
    refresh_token_expect_error,
    user_already_exists_error,
)
from bet_maker.app.api.v1.controllers.auth_controller import auth_router
from bet_maker.app.api.v1.controllers.bets_controller import bets_router
from bet_maker.app.api.v1.controllers.events_controller import events_router
from bet_maker.app.api.v1.controllers.user_controller import user_router
from bet_maker.app.core.custom_exceptions import (
    EventNotFoundError,
    ExpectRefreshTokenError,
    InvalidUsernameOrPasswordError,
    NoMoneyError,
    NotEnoughMoneyError,
    UserWithThisEmailExistsError,
)
from bet_maker.app.repositories.redis_repo import RedisRepo
from bet_maker.app.services.consumer_service import ConsumerService
from shared.configs import all_settings
from shared.configs.rabbitmq import RabbitBaseConnection
from shared.configs.redis import get_redis_connection
from shared.middleware.check_jwt_middleware import CheckJWTAccessMiddleware
from shared.middleware.logging_middleware import LoggerMiddleware
from shared.utils.logger import init_logger

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RabbitBaseConnection(all_settings.rabbit) as rbmq_service:
        redis_connection: Redis = await get_redis_connection()
        redis_service = RedisRepo(redis_connection)
        consumer_service = ConsumerService(rbmq_service, redis_service)

        async def run_tasks() -> None:
            await asyncio.gather(
                consumer_service.consume_forever(all_settings.rabbit.rabbit_rk)
            )

        tasks: asyncio.Task = asyncio.create_task(run_tasks())

        yield
        tasks.cancel()


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserWithThisEmailExistsError, user_already_exists_error)  # type: ignore
    app.add_exception_handler(ExpectRefreshTokenError, refresh_token_expect_error)  # type: ignore
    app.add_exception_handler(InvalidUsernameOrPasswordError, invalid_username_password_error)  # type: ignore
    app.add_exception_handler(EmailNotValidError, email_not_valid_error)  # type: ignore
    app.add_exception_handler(InvalidTokenError, invalid_jwt_error)  # type: ignore
    app.add_exception_handler(EventNotFoundError, event_not_found_error)  # type: ignore
    app.add_exception_handler(NoMoneyError, no_money_error)  # type: ignore
    app.add_exception_handler(NotEnoughMoneyError, not_enough_money_error)  # type: ignore


def init_routers(app: FastAPI) -> None:
    http_bearer = HTTPBearer(auto_error=True)
    app.include_router(auth_router, prefix="/v1")
    app.include_router(events_router, prefix="/v1")
    app.include_router(user_router, prefix="/v1", dependencies=[Depends(http_bearer)])
    app.include_router(bets_router, prefix="/v1", dependencies=[Depends(http_bearer)])


def init_middlewares(app: FastAPI) -> None:
    origins = all_settings.different.bet_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)
    app.add_middleware(CheckJWTAccessMiddleware, jwt_service=get_jwt_service())


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Betting API",
        description="API for betting on sport events",
        version="0.1.0",
        lifespan=lifespan,
    )
    init_logger(all_settings.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
