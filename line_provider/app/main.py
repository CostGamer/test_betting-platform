import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from line_provider.app.api.exception_responses.exceptions import (
    event_not_found_error,
    invalid_id_error,
)
from line_provider.app.api.v1.controllers.events_controller import events_router
from line_provider.app.core.custom_exceptions import EventNotFoundError, InvalidIDError
from line_provider.app.core.schemas.services_protocols import (
    CheckStatusServiceProtocol,
    CreateEventServiceProtocol,
    ProducerServiceProtocol,
)
from line_provider.app.dependencies.container import container
from line_provider.app.storage import events
from shared.configs import all_configs
from shared.middleware.logging_middleware import LoggerMiddleware
from shared.utils.logger import init_logger

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with container() as request_container:
        bg_service: CheckStatusServiceProtocol = await request_container.get(
            CheckStatusServiceProtocol
        )
        create_event_service: CreateEventServiceProtocol = await request_container.get(
            CreateEventServiceProtocol
        )
        producer_service: ProducerServiceProtocol = await request_container.get(
            ProducerServiceProtocol
        )

        async def run_tasks() -> None:
            await asyncio.gather(
                bg_service.check_all_events(),
                create_event_service.create_events_periodically(),
                producer_service.send_periodic_messages(events),
            )

        tasks: asyncio.Task = asyncio.create_task(run_tasks())

        yield
        tasks.cancel()


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidIDError, invalid_id_error)  # type: ignore
    app.add_exception_handler(EventNotFoundError, event_not_found_error)  # type: ignore


def init_routers(app: FastAPI) -> None:
    app.include_router(events_router, prefix="/v1")


def init_middlewares(app: FastAPI) -> None:
    origins = all_configs.different.line_origins

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
        lifespan=lifespan,
    )
    init_logger(all_configs.logging)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    setup_dishka(app=app, container=container)
    logger.info("App created", extra={"app_version": app.version})
    return app
