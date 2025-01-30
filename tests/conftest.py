import random
import string
from collections.abc import AsyncIterator
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from bet_maker.app.main import setup_app as bet_maker_app
from line_provider.app.main import setup_app as line_provider_app
from shared.configs import all_settings


@pytest.fixture(scope="session")
async def line_provider_async_client() -> AsyncGenerator[AsyncClient, None]:
    app = line_provider_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session")
async def bet_maker_async_client() -> AsyncGenerator[AsyncClient, None]:
    app = bet_maker_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session")
async def async_engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        all_settings.database.db_uri, echo=True, future=True, poolclass=NullPool
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def register_token(
    bet_maker_async_client: AsyncClient,
) -> AsyncGenerator[tuple[str, str], None]:
    random_email_body = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    random_email = f"{random_email_body}@mail.com"
    random_password = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    token_issue_data = {"email": random_email, "password": random_password}

    login_response = await bet_maker_async_client.post(
        "/v1/auth/register", json=token_issue_data
    )

    assert login_response.status_code == 200, (
        f"Unexpected status code: {login_response.status_code}. "
        f"Response: {login_response.text}"
    )

    yield random_email, random_password


@pytest.fixture(scope="session")
async def authenticated_token(
    bet_maker_async_client: AsyncClient, register_token: tuple[str, str]
) -> AsyncGenerator[str, None]:
    login_response = await bet_maker_async_client.get(
        "/v1/auth/login",
        params={"email": register_token[0], "password": register_token[1]},
    )

    assert login_response.status_code == 200, (
        f"Unexpected status code: {login_response.status_code}. "
        f"Response: {login_response.text}"
    )

    response_json = login_response.json()

    assert response_json, "No tokens found in response"

    api_key_token = response_json.get("access_token")
    assert api_key_token, "API key token not found in response"

    yield api_key_token


@pytest.fixture(scope="session")
async def set_auth_headers(
    bet_maker_async_client: AsyncClient, authenticated_token: str
) -> AsyncGenerator[AsyncClient, None]:
    bet_maker_async_client.headers.update(
        {"Authorization": f"Bearer {authenticated_token}"}
    )
    yield bet_maker_async_client
