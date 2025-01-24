from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from line_provider.app.api.exception_responses.exceptions import (
    event_not_found_error,
    invalid_id_error,
)
from line_provider.app.api.v1.controllers.events_controller import events_router
from line_provider.app.core.custom_exceptions import EventNotFoundError, InvalidIDError
from shared.configs import all_settings
from shared.middleware.logging import LoggerMiddleware
from shared.utils.logger import init_logger

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidIDError, invalid_id_error)  # type: ignore
    app.add_exception_handler(EventNotFoundError, event_not_found_error)  # type: ignore


def init_routers(app: FastAPI) -> None:
    app.include_router(events_router, prefix="/v1")


def init_middlewares(app: FastAPI) -> None:
    origins = all_settings.different.line_origins

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
        title="Events line API",
        description="API provides information about events",
        version="0.1.0",
    )
    init_logger(all_settings.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
