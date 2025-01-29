from typing import Any

import jwt
from fastapi import Request, status
from jwt.exceptions import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from bet_maker.app.core.custom_exceptions import (
    ExpectAccessTokenError,
    MissingOrBadJWTError,
)
from shared.configs import all_configs
from shared.configs.settings import ACCESS_TOKEN, TOKEN_TYPE_FIELD


class CheckJWTAccessMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = ["/docs", "/openapi.json", "/v1/auth", "/v1/events"]
        self._configs = all_configs

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
                token_payload: dict = await jwt.decode(
                    jwt=token,
                    key=self._configs.jwt.jwt_secret,
                    algorithms=[self._configs.jwt.jwt_algorithm],
                )
            except Exception:
                raise InvalidTokenError

            # if not await self._jwt_service.validation_token_type(
            #     ACCESS_TOKEN, token_payload
            # ):
            if token_payload.get(TOKEN_TYPE_FIELD) != ACCESS_TOKEN:
                raise ExpectAccessTokenError
        except InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid JWT"},
            )
        except MissingOrBadJWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid JWT"},
            )
        except ExpectAccessTokenError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid JWT type"},
            )

        response = await call_next(request)
        return response
