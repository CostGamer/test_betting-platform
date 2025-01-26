from fastapi import Response


class EstablishCookies:
    def __init__(self, response: Response) -> None:
        self._response = response

    async def send_access_token(
        self,
        access_token: str,
    ) -> None:
        self._response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=False,
            samesite="lax",
        )

    async def send_refresh_token(
        self,
        refresh_token: str,
    ) -> None:
        self._response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            httponly=True,
            secure=False,
            samesite="lax",
        )
