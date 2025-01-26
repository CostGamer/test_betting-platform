from logging import getLogger

from email_validator.exceptions_types import EmailNotValidError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError

from bet_maker.app.api.exception_responses.exceptions import (
    email_not_valid_error,
    invalid_jwt_error,
    invalid_username_password_error,
    refresh_token_expect_error,
    user_already_exists_error,
)
from bet_maker.app.api.v1.controllers.auth_controller import auth_router
from bet_maker.app.core.custom_exceptions import (
    ExpectRefreshTokenError,
    InvalidUsernameOrPasswordError,
    UserWithThisEmailExistsError,
)
from shared.configs import all_settings
from shared.middleware.logging_middleware import LoggerMiddleware
from shared.utils.logger import init_logger

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserWithThisEmailExistsError, user_already_exists_error)  # type: ignore
    app.add_exception_handler(ExpectRefreshTokenError, refresh_token_expect_error)  # type: ignore
    app.add_exception_handler(InvalidUsernameOrPasswordError, invalid_username_password_error)  # type: ignore
    app.add_exception_handler(EmailNotValidError, email_not_valid_error)  # type: ignore
    app.add_exception_handler(InvalidTokenError, invalid_jwt_error)  # type: ignore


def init_routers(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/v1")


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


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Betting API",
        description="API for betting on sport events",
        version="0.1.0",
    )
    init_logger(all_settings.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
