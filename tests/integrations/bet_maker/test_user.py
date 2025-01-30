import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user_info(
    set_auth_headers: AsyncClient,
) -> None:
    response = await set_auth_headers.get(
        "/v1/user/",
    )

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    user_data = response.json()

    assert "email" in user_data
    assert "balance" in user_data


@pytest.mark.asyncio
async def test_top_up_user_balance(set_auth_headers: AsyncClient) -> None:
    amount = 50.0
    response = await set_auth_headers.put(
        "/v1/user/balance/top_up",
        params={"amount": amount},
    )

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    balance = response.json()

    assert (
        balance >= amount
    ), f"Expected balance to be at least {amount}, but got {balance}"


@pytest.mark.asyncio
async def test_balance_workflow(set_auth_headers: AsyncClient) -> None:
    response = await set_auth_headers.get("/v1/user/")

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    user_data = response.json()

    assert "email" in user_data
    assert "balance" in user_data

    current_balance = user_data.get("balance", 0)

    min_balance_for_withdraw = 10.0
    top_up_amount = 0.0

    if current_balance < min_balance_for_withdraw:
        top_up_amount = min_balance_for_withdraw - current_balance + 5.0
        top_up_response = await set_auth_headers.put(
            "/v1/user/balance/top_up", params={"amount": top_up_amount}
        )

        assert top_up_response.status_code == 200, (
            f"Expected status code 200 for top up, but got {top_up_response.status_code}. "
            f"Response: {top_up_response.text}"
        )

        new_balance = top_up_response.json()
        assert (
            new_balance == current_balance + top_up_amount
        ), f"Expected new balance {current_balance + top_up_amount}, but got {new_balance}"

    withdraw_amount = 5.0
    withdraw_response = await set_auth_headers.put(
        "/v1/user/balance/withdraw", params={"amount": withdraw_amount}
    )

    assert withdraw_response.status_code == 200, (
        f"Expected status code 200 for withdraw, but got {withdraw_response.status_code}. "
        f"Response: {withdraw_response.text}"
    )

    final_balance = withdraw_response.json()

    assert (
        final_balance == current_balance + top_up_amount - withdraw_amount
    ), f"Expected final balance {current_balance + top_up_amount - withdraw_amount}, but got {final_balance}"
