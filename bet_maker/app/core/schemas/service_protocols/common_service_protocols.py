from typing import Protocol

from fastapi import Request
from pydantic import UUID4


class CommonServiceProtocol(Protocol):
    async def _get_user_id(self, request: Request) -> UUID4:
        """Extract user ID from the JWT token in the request"""
        pass
