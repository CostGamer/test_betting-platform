from email_validator.exceptions_types import EmailNotValidError
from fastapi import Request, status
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from bet_maker.app.core.custom_exceptions import (
    ExpectRefreshTokenError,
    InvalidUsernameOrPasswordError,
    UserWithThisEmailExistsError,
)


async def invalid_username_password_error(
    request: Request, exc: InvalidUsernameOrPasswordError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid password or username"},
    )


async def user_already_exists_error(
    request: Request, exc: UserWithThisEmailExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "This email already in the system"},
    )


async def refresh_token_expect_error(
    request: Request, exc: ExpectRefreshTokenError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Expect refresh jwt"},
    )


async def email_not_valid_error(
    request: Request, exc: EmailNotValidError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Email is not valid"},
    )


async def invalid_jwt_error(request: Request, exc: InvalidTokenError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid jwt"},
    )
