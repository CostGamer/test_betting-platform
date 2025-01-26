from typing import Any

from fastapi import Request, status
from jwt.exceptions import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from bet_maker.app.core.custom_exceptions import (
    ExpectAccessTokenError,
    MissingOrBadJWTError,
)
from bet_maker.app.core.schemas.service_protocols import JWTServiceProtocol
from shared.configs.settings import ACCESS_TOKEN


class CheckJWTAccessMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, jwt_service: JWTServiceProtocol):
        super().__init__(app)
        self._jwt_service = jwt_service
        self.excluded_paths = ["/docs", "/openapi.json", "/jwt"]

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        if any(
            request.url.path.startswith(path.rstrip("/"))
            for path in self.excluded_paths
        ):
            return await call_next(request)

        try:
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise MissingOrBadJWTError
            token = token.split(" ", 1)[1]

            try:
                token_payload = await self._jwt_service.decode_jwt(token)
            except Exception:
                raise InvalidTokenError

            if not await self._jwt_service.validation_token_type(
                ACCESS_TOKEN, token_payload
            ):
                raise ExpectAccessTokenError
        except InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": ""},
            )
        except MissingOrBadJWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": ""},
            )
        except ExpectAccessTokenError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": ""},
            )

        response = await call_next(request)
        return response
