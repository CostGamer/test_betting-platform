from typing import Protocol


class EstablishCookiesProtocol(Protocol):
    async def send_access_token(
        self,
        access_token: str,
    ) -> None:
        """Send the access token to the client as a cookie"""
        pass

    async def send_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        """Send the refresh token to the client as a cookie"""
        pass
