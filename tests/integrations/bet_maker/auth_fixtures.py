# import random
# import string
# import pytest
# from httpx import AsyncClient
# from typing import AsyncGenerator, Tuple


# @pytest.fixture(scope="session")
# async def register_token(bet_maker_async_client: AsyncClient) -> AsyncGenerator[Tuple[str, str], None]:
#     random_login = "".join(
#         random.choice(string.ascii_letters + string.digits) for _ in range(10)
#     )
#     random_password = "".join(
#         random.choice(string.ascii_letters + string.digits) for _ in range(10)
#     )
#     token_issue_data = {"login": random_login, "password": random_password}

#     login_response = await bet_maker_async_client.post(
#         "/v1/auth/register", params=token_issue_data
#     )

#     assert login_response.status_code == 200, (
#         f"Unexpected status code: {login_response.status_code}. "
#         f"Response: {login_response.text}"
#     )

#     yield random_login, random_password


# @pytest.fixture(scope="session")
# async def authenticated_token(
#     bet_maker_async_client: AsyncClient, register_token: Tuple[str, str]
# ) -> AsyncGenerator[str, None]:
#     login_response = await bet_maker_async_client.get(
#         "/v1/auth/login", params={"login": register_token[0], "password": register_token[1]}
#     )

#     assert login_response.status_code == 200, (
#         f"Unexpected status code: {login_response.status_code}. "
#         f"Response: {login_response.text}"
#     )

#     response_json = login_response.json()

#     assert response_json, "No tokens found in response"

#     api_key_token = response_json.get("access_token")
#     assert api_key_token, "API key token not found in response"

#     yield api_key_token


# @pytest.fixture(scope="session")
# async def set_auth_headers(
#     bet_maker_async_client: AsyncClient, authenticated_token: str
# ) -> AsyncGenerator[AsyncClient, None]:
#     bet_maker_async_client.headers.update({"Authorization": f"Bearer {authenticated_token}"})
#     yield bet_maker_async_client
