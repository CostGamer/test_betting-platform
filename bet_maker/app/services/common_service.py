from uuid import UUID

from fastapi import Request
from pydantic import UUID4

from bet_maker.app.core.schemas.service_protocols import JWTServiceProtocol


class CommonService:
    def __init__(self, jwt_service: JWTServiceProtocol):
        self._jwt_service = jwt_service

    async def _get_user_id(self, request: Request) -> UUID4:
        token = await self._jwt_service.get_token_from_response(request)
        jwt_payload = await self._jwt_service.decode_jwt(token)
        return UUID(jwt_payload.get("sub"), version=4)
