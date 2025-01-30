from uuid import UUID

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_event(line_provider_async_client: AsyncClient) -> None:
    event_id = "547e95a4-0afc-46d2-8c32-c757cc6bb5d9"

    response = await line_provider_async_client.get(f"/v1/events/event/{event_id}")

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )
    response_json = response.json()

    assert response_json["event_id"] == event_id
    assert response_json["name"] == "Real Madrid - Barcelona"
    assert float(response_json["coefficient"]) == float("1.51")
    assert response_json["status"] == 1


@pytest.mark.asyncio
async def test_get_events(line_provider_async_client: AsyncClient) -> None:
    expected_event_names = [
        "Real Madrid - Barcelona",
        "Liverpool - Chelsea",
        "Paris Saint-Germain - Bayern Munich",
    ]

    response = await line_provider_async_client.get("/v1/events/")

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_json = response.json()

    assert len(response_json) == len(expected_event_names), (
        f"Expected {len(expected_event_names)} events, but got {len(response_json)}. "
        f"Response: {response_json}"
    )

    actual_event_names = [event["name"] for event in response_json]

    for expected_name in expected_event_names:
        assert expected_name in actual_event_names, (
            f"Expected event with name {expected_name} not found in the response. "
            f"Response names: {actual_event_names}"
        )


@pytest.mark.asyncio
async def test_create_new_event(line_provider_async_client: AsyncClient) -> None:
    event_data = {
        "name": "Test Event",
        "coefficient": "1.5",
        "deadline": 40,
        "status": 1,
    }

    response = await line_provider_async_client.post(
        "/v1/events/create_event", json=event_data
    )

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_text = response.text.strip('"')
    print(response_text)
    try:
        uuid_obj = UUID(response_text)
    except ValueError:
        raise AssertionError("Invalid UUID format")

    event_response = await line_provider_async_client.get(
        f"/v1/events/event/{uuid_obj}"
    )

    assert event_response.status_code == 200, (
        f"Expected status code 200, but got {event_response.status_code}. "
        f"Response: {event_response.text}"
    )

    event_data_response = event_response.json()

    assert event_data_response["name"] == event_data["name"]
