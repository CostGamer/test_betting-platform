from fastapi import Request, status
from fastapi.responses import JSONResponse

from line_provider.app.core.custom_exceptions import EventNotFoundError, InvalidIDError


async def invalid_id_error(request: Request, exc: InvalidIDError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "UUID format is incorrect"},
    )


async def event_not_found_error(
    request: Request, exc: EventNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Event not found"},
    )
